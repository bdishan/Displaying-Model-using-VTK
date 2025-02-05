import vtk

# Load the STL model
reader = vtk.vtkSTLReader()
reader.SetFileName("Toothless.stl")  # Replace with the correct path if not in the same folder
reader.Update()

# getting number of vertices
poly_data = reader.GetOutput()
num_vertices = poly_data.GetNumberOfPoints()
print(f"Number of vertices: {num_vertices}")


# Create mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Wireframe actor
actor_wireframe = vtk.vtkActor()
actor_wireframe.SetMapper(mapper)
actor_wireframe.GetProperty().SetRepresentationToWireframe()
actor_wireframe.GetProperty().SetColor(0.5, 0.5, 0.5)  # Gray color
actor_wireframe.GetProperty().LightingOff()  # Disable lighting for wireframe

# Flat shading actor
actor_flat = vtk.vtkActor()
actor_flat.SetMapper(mapper)
actor_flat.GetProperty().SetInterpolationToFlat()
actor_flat.GetProperty().SetColor(0.5, 0.5, 0.5)  # Gray color

# Gouraud shading actor
actor_gouraud = vtk.vtkActor()
actor_gouraud.SetMapper(mapper)
actor_gouraud.GetProperty().SetInterpolationToGouraud()
actor_gouraud.GetProperty().SetColor(0.5, 0.5, 0.5)  # Gray color

# Phong shading actor
actor_phong = vtk.vtkActor()
actor_phong.SetMapper(mapper)
actor_phong.GetProperty().SetInterpolationToPhong()
actor_phong.GetProperty().SetColor(0.5, 0.5, 0.5)  # Gray color

# Create renderers for each viewport
ren_wireframe = vtk.vtkRenderer()
ren_wireframe.SetViewport(0.0, 0.5, 0.5, 1.0)  # Top-left
ren_wireframe.AddActor(actor_wireframe)
ren_wireframe.SetBackground(1.0, 1.0, 1.0)  # White background

ren_flat = vtk.vtkRenderer()
ren_flat.SetViewport(0.5, 0.5, 1.0, 1.0)  # Top-right
ren_flat.AddActor(actor_flat)
ren_flat.SetBackground(1.0, 1.0, 1.0)  # White background

ren_gouraud = vtk.vtkRenderer()
ren_gouraud.SetViewport(0.0, 0.0, 0.5, 0.5)  # Bottom-left
ren_gouraud.AddActor(actor_gouraud)
ren_gouraud.SetBackground(1.0, 1.0, 1.0)  # White background

ren_phong = vtk.vtkRenderer()
ren_phong.SetViewport(0.5, 0.0, 1.0, 0.5)  # Bottom-right
ren_phong.AddActor(actor_phong)
ren_phong.SetBackground(1.0, 1.0, 1.0)  # White background

# Create a render window and add the renderers
render_window = vtk.vtkRenderWindow()
render_window.SetSize(1600, 1600)  # Set canvas size to 1600x1600
render_window.AddRenderer(ren_wireframe)
render_window.AddRenderer(ren_flat)
render_window.AddRenderer(ren_gouraud)
render_window.AddRenderer(ren_phong)

# Render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(render_window)

# Add a callback to capture the JPEG after interaction ends
def save_screenshot_callback(obj, event):
    # Capture the rendered scene as an image
    window_to_image_filter = vtk.vtkWindowToImageFilter()
    window_to_image_filter.SetInput(render_window)
    window_to_image_filter.Update()

    # Save the rendered image to a JPEG file
    jpeg_writer = vtk.vtkJPEGWriter()
    jpeg_writer.SetFileName("output.jpg")
    jpeg_writer.SetInputConnection(window_to_image_filter.GetOutputPort())
    jpeg_writer.Write()
    print("Screenshot saved as 'output.jpg'.")

# Bind the callback to the "EndInteractionEvent"
iren.AddObserver("EndInteractionEvent", save_screenshot_callback)

# Start the interaction
render_window.Render()
iren.Initialize()
iren.Start()
