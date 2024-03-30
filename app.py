import tkinter as tk
from tkinter import filedialog , simpledialog
import vtk

class STLViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dental STL Viewer")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.choose_file_btn = tk.Button(self.frame, text="Choose File", command=self.load_stl_file)
        self.choose_file_btn.pack()

    def load_stl_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
        if file_path:
            # Ask the user if the STL is for an upper or lower chain
            chain_type = simpledialog.askstring("Chain Type", "Is this an upper or lower chain? (upper/lower)")
            if chain_type:
                chain_type = chain_type.lower()
                self.display_stl(file_path, chain_type)
            else:
                tk.messagebox.showerror("Error", "You must specify 'upper' or 'lower'.")

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

        # Initialize the render window interactor and start the rendering loop
        self.render_window_interactor.Initialize()
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




    def setup_rotation_buttons(self):
        # Create a new window for the rotation controls
        self.control_window = tk.Toplevel(self.root)
        self.control_window.title("Rotate Model")

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

    
    def rotate_model(self, axis, angle):
        if axis == 'x':
            self.renderer.GetActiveCamera().Elevation(angle)
        elif axis == 'y':
            self.renderer.GetActiveCamera().Azimuth(angle)
        
        self.renderer.ResetCameraClippingRange()
        self.render_window.Render()

if __name__ == "__main__":
    root = tk.Tk()
    app = STLViewerApp(root)
    root.mainloop()
