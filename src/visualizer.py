# references
# https://stackoverflow.com/questions/66608152/scaling-along-a-single-axis-in-open3d
# https://www.open3d.org/html/python_api/open3d.visualization.html
# https://www.open3d.org/html/tutorial/Basic/index.html
# https://www.open3d.org/html/tutorial/Advanced/index.html
# https://github.com/mxagar/open3d_guide/blob/main/notebooks/04_Transformations.ipynb

# import sys
# import os

# # Add the directory containing 'examples' to the Python path
# notebook_directory = os.getcwd()
# parent_directory = os.path.dirname(notebook_directory)  # Parent directory
# sys.path.append(parent_directory)

# import open3d as o3d
# import numpy as np

# # Here, the same file is opened locally
# pcd = o3d.io.read_point_cloud("open3d_guide/models/fragment.ply")
# print(pcd) # 196133 points
# print(np.asarray(pcd.points))

# # A new visualization window is opened
# # Keys:
# #  [/]          : Increase/decrease field of view.
# #  R            : Reset view point.
# #  Ctrl/Cmd + C : Copy current view status into the clipboard.
# #  Ctrl/Cmd + V : Paste view status from clipboard.
# #  Q, Esc       : Exit window.
# #  H            : Print help message.
# #  P, PrtScn    : Take a screen capture.
# #  D            : Take a depth capture.
# #  O            : Take a capture of current rendering settings.
# # IMPORTANT: Press Q to exit the viewer; the notebook cell waits for that!
# o3d.visualization.draw_geometries([pcd],
#                                   zoom=0.3412,
#                                   front=[0.4257, -0.2125, -0.8795],
#                                   lookat=[2.6172, 2.0475, 1.532],
#                                   up=[-0.0694, -0.9768, 0.2024])

# # We can inspect the docstring of each function with help()
# # help(o3d.visualization.draw_geometries)

# # In-Notebook web visualizer (but with a worse quality)
# # o3d.web_visualizer.draw(pcd,                                  
# #                         lookat=[2.6172, 2.0475, 1.532],
# #                         up=[-0.0694, -0.9768, 0.2024])

# # IO Pointcloud
# pcd = o3d.io.read_point_cloud("open3d_guide/models/fragment.pcd")
# print(pcd)
# # Save file
# # The format is passed in the extension, or, optionally in the argument format='xyz'
# # Supported formats: 
# # xyz: [x, y, z]
# # xyzn: [x, y, z, nx, ny, nz]
# # xyzrgb: [x, y, z, r, g, b]
# # pts: [x, y, z, i, r, g, b]
# # ply
# # pcd
# o3d.io.write_point_cloud("copy_of_fragment.pcd", pcd)

# # IO Mesh
# mesh = o3d.io.read_triangle_mesh("open3d_guide/models/monkey.ply")
# print(mesh)
# # Save file
# # The format is passed in the extension
# # Supported formats: 
# # ply, stl, obj, off, gltf/glb
# o3d.io.write_triangle_mesh("copy_monkey.ply", mesh)

# # IO Image
# img = o3d.io.read_image("open3d_guide/models/lenna.png")
# print(img)
# # Save file
# # Supported formats: JPG, PNG
# o3d.io.write_image("copy_of_lena.jpg", img)

# # We can download data using `o3d.data`; a list of all possible models is provided here:
# # https://www.open3d.org/docs/release/python_api/open3d.data.html
# armadillo = o3d.data.ArmadilloMesh()
# armadillo_mesh = o3d.io.read_triangle_mesh(armadillo.path)
# bunny = o3d.data.BunnyMesh()
# bunny_mesh = o3d.io.read_triangle_mesh(bunny.path)

# # Visualize the mesh
# print(bunny_mesh)
# o3d.visualization.draw_geometries([bunny_mesh], window_name='3D Mesh Visualization')

#########################

# import open3d as o3d

# vis = o3d.visualization.Visualizer()
# vis.create_window("test", width=800, height=600)

# #mesh = o3d.geometry.TriangleMesh.create_box()
# mesh = o3d.geometry.TriangleMesh.create_sphere(0.8)

# mesh.paint_uniform_color([1, 0.7, 0])
# mesh.compute_vertex_normals()

# vis.add_geometry(mesh)

############################

# Render colored wireframe of a cube
# Render multiple cubes
# Setup cube position, orientation and scale once
# Setup cube position, orientation and scale in realtime
# Grab a point cloud from the depth map
# Colorize the point cloud using the image
# Render a point cloud
# Create a hashmap to store bounding boxes

# Rendering loop
# i = 0
# multiplier = 1
# while True:
#     i += 1
#     if i % 100 == 0:
#         multiplier *= -1
#     #mesh.translate([0.001 * multiplier, 0, 0])
#     mesh.scale(0.999, center=mesh.get_center())
#     # Move cube slightly to show that the rendering is real-time
#     vis.update_geometry(mesh)
#     vis.poll_events()
#     vis.update_renderer()


#########################

    
#o3d.visualization.draw(mesh, raw_mode=True)

# if __name__ == '__main__':
#     # Create Open3d visualization window
#     vis.create_window()
#     # initialization

#     vis.get_render_option().background_color = [0.75, 0.75, 0.75]
#     vis.get_render_option().mesh_show_back_face = True

#     # adding geometries : 
#     #for g in geometries:
#     vis.add_geometry(mesh)

#     while True:
#         # updating geometries:
#         # ...
        
#         #for g in geometries:
#             # update
#         #pointcloud.points = mesh.points
#         vis.update_geometry(pointcloud)

#         vis.poll_events()
#         vis.update_renderer()


# import cv2
# import numpy as np
# import transform
# import camera
# import util

# class Visualizer:
#     def __init__(self, camera):
#         self.camera = camera

#     # TODO: fix the projection of points that fall behind the camera
#     def project_points(self, points):
#         # Project the 3D points to the 2D image

#         tvec = self.camera.transform.get_tvec()
#         #print("Visualizer.project_points.tvec\n", tvec)
#         rvec = self.camera.transform.get_rvec()
#         #print("Visualizer.project_points.rvec\n", rvec)
#         intrinsic = self.camera.intrinsic_matrix
#         #print("Visualizer.project_points.intrinsic\n", intrinsic)

#         points_2D = cv2.projectPoints(
#             points,
#             rvec,
#             tvec,
#             intrinsic,
#             None
#         )[0]

#         return points_2D
    
#     def project_lines(self, lines):
#         # Project the 3D lines to the 2D image
#         lines_2D = []
#         for line in lines:
#             points_2D = self.project_points(line)
#             lines_2D.append(points_2D)

#         return lines_2D
    
#     def project_cubes(self, cubes):
#         # Project the 3D cubes to the 2D image
#         cubes_2D = []
#         for cube in cubes:
#             lines_2D = self.project_lines(cube)
#             cubes_2D.append(lines_2D)

#         return cubes_2D
    
#     def draw_floor_grid(self, image, size=10, step=1, color=(255, 255, 255)):
        
#         # Draw the floor grid
#         for i in range(-size, size + 1, step):
            
#             # Create the line
#             line_3D_z = np.array([[i, 0, -size], [i, 0, size]], dtype=np.float32)
#             line_3D_x = np.array([[-size, 0, i], [size, 0, i]], dtype=np.float32)

#             # Project the line to the 2D image
#             line_2D_z = self.project_points(line_3D_z)
#             line_2D_x = self.project_points(line_3D_x)

#             box = [0, 0, image.shape[1], image.shape[0]]

#             p1_z = line_2D_z.astype(int)[0][0]
#             p2_z = line_2D_z.astype(int)[1][0]
#             p1_z_clipped, p2_z_clipped = util.clip(p1_z, p2_z, box)
#             if(p1_z_clipped is not None and p2_z_clipped is not None):
#                 p1_z[0] = p1_z_clipped[0]
#                 p1_z[1] = p1_z_clipped[1]
#                 p2_z[0] = p2_z_clipped[0]
#                 p2_z[1] = p2_z_clipped[1]
#                 cv2.line(image, p1_z, p2_z, color, 1)

#             p1_x = line_2D_x.astype(int)[0][0]
#             p2_x = line_2D_x.astype(int)[1][0]
#             p1_x_clipped, p2_x_clipped = util.clip(p1_x, p2_x, box)
#             if(p1_x_clipped is not None and p2_x_clipped is not None):
#                 p1_x[0] = p1_x_clipped[0]
#                 p1_x[1] = p1_x_clipped[1]
#                 p2_x[0] = p2_x_clipped[0]
#                 p2_x[1] = p2_x_clipped[1]
#                 cv2.line(image, p1_x, p2_x, color, 1)                    
    

#     def show(self):

#         # Create an opencv window
#         cv2.namedWindow('Visualizer')

#         # # Move camera forward
#         # self.camera.transform.move_forward(-0.01)
#         # self.camera.transform.move_upward(-0.005)
#         # self.camera.transform.move_sideward(0.005)

#         # Create a blank image
#         image = np.ones((self.camera.height, self.camera.width, 3), dtype=np.uint8)*220

#         # Draw the floor grid
#         self.draw_floor_grid(image, 8, 4, (10, 10, 10))

#         # Show the image
#         cv2.imshow('Visualizer', image)

# camera = camera.Camera(1920, 800)

# visualizer = Visualizer(camera)

# key = 0
# velocity = 0.1

# while True:
#     # Press 'wasdqe' to move the camera and 'esc' to quit
#     if key == ord('w'): camera.transform.move_forward(-velocity)
#     if key == ord('s'): camera.transform.move_forward(velocity)
#     if key == ord('a'): camera.transform.move_sideward(-velocity)
#     if key == ord('d'): camera.transform.move_sideward(velocity)
#     if key == ord('q'): camera.transform.move_upward(velocity)
#     if key == ord('e'): camera.transform.move_upward(-velocity)
#     if key == 27: break
        
#     visualizer.show()

#     key = cv2.waitKey(1) & 0xFF

##########################################

# import copy

# # Open3D also supports a general transformation 
# # defined by a 4×4 homogeneous transformation matrix using the method transform.
# mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
# T = np.eye(4)
# #T[:3, :3] = mesh.get_rotation_matrix_from_xyz((0, np.pi / 3, np.pi / 2))
# T[0, 0] = 4
# T[1, 1] = 2
# T[2, 2] = 2
# T[0, 3] = 2
# T[1, 3] = 2
# print(T)
# mesh_t = copy.deepcopy(mesh).transform(T)
# o3d.visualization.draw_geometries([mesh, mesh_t])

##########################################


import numpy as np
import open3d as o3d
import geometry as geo

def create_line_set(color):
    # Move cube slightly to show that the rendering is real-time
    x = -103.5
    y = -100.5
    z = -110.5
    h = 2
    w = 1
    l = 0.5
    r = 0
    points = box_center_to_corner([x,y,z,h,w,l,r])

    # Our lines span from points 0 to 1, 1 to 2, 2 to 3, etc...
    lines = [[0, 1], [1, 2], [2, 3], [0, 3],
             [4, 5], [5, 6], [6, 7], [4, 7],
             [0, 4], [1, 5], [2, 6], [3, 7]]

    colors = [color for _ in range(len(lines))]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)

    return line_set

def box_center_to_corner(box):
    # To return
    corner_boxes = np.zeros((8, 3))

    translation = box[0:3]
    h, w, l = box[3], box[4], box[5]
    rotation = box[6]

    # Create a bounding box outline
    bounding_box = np.array([
        [-l/2, -l/2, l/2, l/2, -l/2, -l/2, l/2, l/2],
        [w/2, -w/2, -w/2, w/2, w/2, -w/2, -w/2, w/2],
        [-h/2, -h/2, -h/2, -h/2, h/2, h/2, h/2, h/2]])

    # Standard 3x3 rotation matrix around the Z axis
    rotation_matrix = np.array([
        [np.cos(rotation), -np.sin(rotation), 0.0],
        [np.sin(rotation), np.cos(rotation), 0.0],
        [0.0, 0.0, 1.0]])

    # Repeat the [x, y, z] eight times
    eight_points = np.tile(translation, (8, 1))

    # Translate the rotated bounding box by the
    # original center position to obtain the final box    
    corner_box = np.dot(rotation_matrix, bounding_box)# + eight_points.transpose()

    return corner_box.transpose()

# Create a visualization object and window
vis = o3d.visualization.Visualizer()
vis.create_window()

geometry = geo.Geometry()
top_left_front = np.array([0, 0, 0])
bottom_right_back = np.array([1, 1, 1])
label = "person"
box = geometry.create_bounding_box(top_left_front, bottom_right_back, label)

line_set = create_line_set([0, 1, 0])

# Display the bounding boxes:
vis.add_geometry(box.line_set)
#vis.add_geometry(line_set)

i = 0
multiplier = 1
while True:

    i += 1
    if i % 1000 == 0:
        multiplier *= -1
    
    #line_set.translate([0.001 * multiplier, 0, 0])
    #line_set.scale(0.999, center=line_set.get_center())

    box.line_set.points = o3d.utility.Vector3dVector(
    np.asarray(box.line_set.points) * np.array([1.001, 1., 1.]) )

    vis.update_geometry(box.line_set)
    vis.poll_events()
    vis.update_renderer()