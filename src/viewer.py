import glfw

# Initialize the library
glfw.init()

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(640, 480, "Hello World", None, None)
if not window:
    glfw.terminate()

# Make the window's context current
glfw.make_context_current(window)

# Loop until the user closes the window
while not glfw.window_should_close(window):
    # Render here, e.g. using pyOpenGL

    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

glfw.terminate()