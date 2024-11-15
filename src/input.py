
import threading
from pynput import mouse, keyboard

class Input:
    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0

    def start(self):
        # Start mouse listener in a separate thread
        mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        mouse_thread = threading.Thread(target=mouse_listener.start)
        mouse_thread.daemon = True
        mouse_thread.start()

        # Start keyboard listener in a separate thread
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        keyboard_thread = threading.Thread(target=keyboard_listener.start)
        keyboard_thread.daemon = True
        keyboard_thread.start()

    # Define callback functions for mouse events
    def on_move(x, y):
        mouse_x = x
        mouse_y = y
        #print(f"Mouse moved to ({x}, {y})")

    def on_click(x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")
        else:
            print(f"Mouse released at ({x}, {y}) with {button}")

    def on_scroll(x, y, dx, dy):
        print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

    # Define callback functions for keyboard events
    def on_press(key):
        try:
            print(f"Key pressed: {key.char}")
        except AttributeError:
            print(f"Special key pressed: {key}")

    def on_release(key):
        print(f"Key released: {key}")
        if key == keyboard.Key.esc:
            # Stop listener
            return False