# Window: tracks the active OS window to associate detections with the foreground application
import pygetwindow as gw

class Window:
    def __init__(self):
        self.active_window = gw.getActiveWindow()  
        self.current_window = self.active_window      

    def process(self):
        self.current_window = gw.getActiveWindow()

    def show(self):
        # Print the title of the active window
        if self.active_window != None and self.current_window != None and self.active_window.title != self.current_window.title:
            self.active_window = self.current_window
            print(f"Current focused window name: {self.active_window.title}")