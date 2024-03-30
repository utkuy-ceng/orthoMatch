import tkinter as tk
from tkinter import filedialog
import vtk

class STLViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ortoMatch")

        # Center the window
        self.center_window(250, 100)

        # Add a "Choose File" button
        self.choose_file_btn = tk.Button(self.root, text="Choose File", command=self.choose_and_display_stl)
        self.choose_file_btn.pack(expand=True)

    def center_window(self, width=300, height=200):
        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position to center the window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def choose_and_display_stl(self):
        # Open a file dialog to select the STL file
        file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
        if file_path:
            self.display_stl(file_path)

    def display_stl(self, file_path):
        # The same vtk code as before to display the STL
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_path)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)
        renderer.SetBackground(0.1, 0.2, 0.4)

        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.SetSize(800, 600)

        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(render_window)

        interactor.Initialize()
        render_window.Render()
        interactor.Start()

if __name__ == "__main__":
    root = tk.Tk()
    app = STLViewerApp(root)
    root.mainloop()
