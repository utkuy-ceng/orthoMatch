import tkinter as tk
from tkinter import filedialog , simpledialog
import vtk
from PIL import Image, ImageTk  # Make sure to install pillow for ImageTk: pip install pillow


class STLViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dental STL Viewer")
        
        # Center the main window on the screen
        self.center_window(200, 35)  # Assuming a desired size of 800x800 for the VTK window
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.choose_file_btn = tk.Button(self.frame, text="Choose File", command=self.load_stl_file)
        self.choose_file_btn.pack()
    
    def center_window(self, width, height):
        # Calculate position x, y to center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def load_stl_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
        if file_path:
            # Determine the chain type based on the filename
            if "_u" in file_path:
                chain_type = "upper"
            elif "_l" in file_path:
                chain_type = "lower"
            else:
                # Ask the user if the STL is for an upper or lower chain
                chain_type = simpledialog.askstring("Chain Type", "Is this an upper or lower chain? (upper/lower)")
                if chain_type:
                    chain_type = chain_type.lower()
                else:
                    tk.messagebox.showerror("Error", "You must specify 'upper' or 'lower'.")
                    return  # Exit the function if no chain type is specified
            
            # Display the STL file with the appropriate view
            self.display_stl(file_path, chain_type)


    def display_stl(self, file_path, chain_type):
        # Read the STL file
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_path)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(actor)
        self.renderer.SetBackground(0.1, 0.2, 0.4)
        self.render_window = vtk.vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.SetSize(800, 800)
        self.render_window_interactor = vtk.vtkRenderWindowInteractor()
        self.render_window_interactor.SetRenderWindow(self.render_window)
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.render_window_interactor.SetInteractorStyle(style)
        self.render_window_interactor.Initialize()

        # Adjust camera based on the chain type
        if chain_type == "upper":
            self.adjust_camera_for_bottom_view()
        elif chain_type == "lower":
            self.adjust_camera_for_top_view()
        
        self.render_window.Render()

        # Setup the rotation buttons once the file is loaded
        self.setup_rotation_buttons()

    def adjust_camera_for_top_view(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, 1)  # Position the camera above the model
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin
        camera.SetViewUp(0, 1, 0)  # Set the up direction to "y"
        self.renderer.ResetCamera()  # Adjust the camera to see the whole model

    def adjust_camera_for_bottom_view(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, -1)  # Position the camera below the model
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin
        camera.SetViewUp(0, -1, 0)  # Invert the up direction to view from below
        self.renderer.ResetCamera()  # Adjust the camera to see the whole model


    def adjust_camera_for_top_view(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, 1)  # Position the camera above the model
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin
        camera.SetViewUp(0, 1, 0)  # Set the up direction to "y"
        self.renderer.ResetCamera()  # Adjust the camera to see the whole model
    
    def adjust_camera_for_bottom_view(self):
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, 0, -1)  # Position the camera below the model
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin
        camera.SetViewUp(0, -1, 0)  # Invert the up direction to view from below
        self.renderer.ResetCamera()  # Adjust the camera to see the whole model




    def setup_rotation_buttons(self):
        # Create a new window for the rotation controls
        self.control_window = tk.Toplevel(self.root)
        self.control_window.title("Rotate Model")
        
        # Position the rotation control window at the top-right of the main window
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()
        self.control_window.geometry(f'+{x}+{y}')

        # Button to rotate the model up (about the x-axis)
        rotate_up_btn = tk.Button(self.control_window, text="Rotate Up", command=lambda: self.rotate_model('x', -10))
        rotate_up_btn.pack(side=tk.TOP)

        # Button to rotate the model down (about the x-axis)
        rotate_down_btn = tk.Button(self.control_window, text="Rotate Down", command=lambda: self.rotate_model('x', 10))
        rotate_down_btn.pack(side=tk.BOTTOM)

        # Button to rotate the model left (about the y-axis)
        rotate_left_btn = tk.Button(self.control_window, text="Rotate Left", command=lambda: self.rotate_model('y', 10))
        rotate_left_btn.pack(side=tk.LEFT)

        # Button to rotate the model right (about the y-axis)
        rotate_right_btn = tk.Button(self.control_window, text="Rotate Right", command=lambda: self.rotate_model('y', -10))
        rotate_right_btn.pack(side=tk.RIGHT)

        capture_btn = tk.Button(self.control_window, text="Capture", command=self.capture_view)
        capture_btn.pack(side=tk.BOTTOM)

    
    def rotate_model(self, axis, angle):
        if axis == 'x':
            self.renderer.GetActiveCamera().Elevation(angle)
        elif axis == 'y':
            self.renderer.GetActiveCamera().Azimuth(angle)
        
        self.renderer.ResetCameraClippingRange()
        self.render_window.Render()

    def capture_view(self):
        # Setup the filter to capture the window
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.render_window)
        w2if.Update()
        
        # Setup the image writer to write the captured image to a file
        writer = vtk.vtkPNGWriter()
        writer.SetFileName("captured_model.png")
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.Write()
        
        # Display the captured image in a new window or replace the current STL model view
        self.display_captured_image("captured_model.png")

    def display_captured_image(self, image_path):
        # This method opens a new window to display the captured image
            image_window = tk.Toplevel(self.root)
            image_window.title("Captured Image")
            
            # Use PIL to open image and convert to PhotoImage
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            
            label = tk.Label(image_window, image=photo)
            label.image = photo  # Keep a reference!
            label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = STLViewerApp(root)
    root.mainloop()
