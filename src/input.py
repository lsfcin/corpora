# Input: threaded mouse and keyboard listener for real-time interaction

import threading
from pynput import mouse, keyboard

class Input:
    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0

        # Start mouse listener in a separate thread
        self.mouse_listener = mouse.Listener(
            #on_move=self.__on_move, # on_move event is deactivated
            on_click=self.__on_click,
            on_scroll=self.__on_scroll)
        self.mouse_thread = threading.Thread(target=self.mouse_listener.start)
        self.mouse_thread.daemon = True
        self.mouse_thread.start()

        # Start keyboard listener in a separate thread
        self.keyboard_listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release)
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener.start)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()

    # Define callback functions for mouse events
    def __on_move(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
        print(f"Mouse moved to ({x}, {y})")

    def __on_click(self, x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")
        else:
            print(f"Mouse released at ({x}, {y}) with {button}")

    def __on_scroll(self, x, y, dx, dy):
        print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

    # Define callback functions for keyboard events
    def __on_press(self, key):
        try:
            print(f"Key pressed: {key.char}")
        except AttributeError:
            print(f"Special key pressed: {key}")

    def __on_release(self, key):
        print(f"Key released: {key}")
        if key == keyboard.Key.esc:
            # Stop listener
            return False