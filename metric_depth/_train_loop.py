# Training loop and evaluation helpers for DepthAnythingV2 metric depth fine-tuning.
import os
import random

import torch
import torch.distributed as dist
import torch.nn.functional as F

from util.metric import eval_depth


def run_train_epoch(model, trainloader, optimizer, criterion, args, rank, writer, epoch, total_iters, logger):
    """Run one training epoch. Returns total loss for the epoch."""
    model.train()
    total_loss = 0

    for i, sample in enumerate(trainloader):
        optimizer.zero_grad()

        img, depth, valid_mask = sample['image'].cuda(), sample['depth'].cuda(), sample['valid_mask'].cuda()

        if random.random() < 0.5:
            img = img.flip(-1)
            depth = depth.flip(-1)
            valid_mask = valid_mask.flip(-1)

        pred = model(img)

        loss = criterion(pred, depth, (valid_mask == 1) & (depth >= args.min_depth) & (depth <= args.max_depth))

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        iters = epoch * len(trainloader) + i

        lr = args.lr * (1 - iters / total_iters) ** 0.9

        optimizer.param_groups[0]["lr"] = lr
        optimizer.param_groups[1]["lr"] = lr * 10.0

        if rank == 0 and writer is not None:
            writer.add_scalar('train/loss', loss.item(), iters)

        if rank == 0 and i % 100 == 0:
            logger.info('Iter: {}/{}, LR: {:.7f}, Loss: {:.3f}'.format(
                i, len(trainloader), optimizer.param_groups[0]['lr'], loss.item()))

    return total_loss


def run_eval_epoch(model, valloader, args):
    """Run evaluation over the validation set. Returns (results dict, nsamples tensor)."""
    model.eval()

    results = {
        'd1': torch.tensor([0.0]).cuda(), 'd2': torch.tensor([0.0]).cuda(),
        'd3': torch.tensor([0.0]).cuda(), 'abs_rel': torch.tensor([0.0]).cuda(),
        'sq_rel': torch.tensor([0.0]).cuda(), 'rmse': torch.tensor([0.0]).cuda(),
        'rmse_log': torch.tensor([0.0]).cuda(), 'log10': torch.tensor([0.0]).cuda(),
        'silog': torch.tensor([0.0]).cuda()
    }
    nsamples = torch.tensor([0.0]).cuda()

    for i, sample in enumerate(valloader):

        img, depth, valid_mask = sample['image'].cuda().float(), sample['depth'].cuda()[0], sample['valid_mask'].cuda()[0]

        with torch.no_grad():
            pred = model(img)
            pred = F.interpolate(pred[:, None], depth.shape[-2:], mode='bilinear', align_corners=True)[0, 0]

        valid_mask = (valid_mask == 1) & (depth >= args.min_depth) & (depth <= args.max_depth)

        if valid_mask.sum() < 10:
            continue

        cur_results = eval_depth(pred[valid_mask], depth[valid_mask])

        for k in results.keys():
            results[k] += cur_results[k]
        nsamples += 1

    return results, nsamples


def reduce_eval_results(results, nsamples):
    """Barrier + all-reduce eval tensors across ranks. Must be called by ALL ranks."""
    torch.distributed.barrier()

    for k in results.keys():
        dist.reduce(results[k], dst=0)
    dist.reduce(nsamples, dst=0)

    return results, nsamples


def log_and_save(results, nsamples, previous_best, model, optimizer, epoch, args, writer, logger):
    """Log eval results to TensorBoard/console and save checkpoint. Rank-0 only."""
    logger.info('==========================================================================================')
    logger.info('{:>8}, {:>8}, {:>8}, {:>8}, {:>8}, {:>8}, {:>8}, {:>8}, {:>8}'.format(*tuple(results.keys())))
    logger.info('{:8.3f}, {:8.3f}, {:8.3f}, {:8.3f}, {:8.3f}, {:8.3f}, {:8.3f}, {:8.3f}, {:8.3f}'.format(
        *tuple([(v / nsamples).item() for v in results.values()])))
    logger.info('==========================================================================================')
    print()

    for name, metric in results.items():
        writer.add_scalar(f'eval/{name}', (metric / nsamples).item(), epoch)

    for k in results.keys():
        if k in ['d1', 'd2', 'd3']:
            previous_best[k] = max(previous_best[k], (results[k] / nsamples).item())
        else:
            previous_best[k] = min(previous_best[k], (results[k] / nsamples).item())

    checkpoint = {
        'model': model.state_dict(),
        'optimizer': optimizer.state_dict(),
        'epoch': epoch,
        'previous_best': previous_best,
    }
    torch.save(checkpoint, os.path.join(args.save_path, 'latest.pth'))

    return previous_best
