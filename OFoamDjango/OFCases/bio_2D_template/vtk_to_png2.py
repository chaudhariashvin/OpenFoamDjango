import pyvista as pv
import os
pv.start_xvfb()
# List available time directories
dir = os.listdir('postProcessing/planes')
dir = [int(value) for value in dir]

# Find the maximum time directory
max_d = max(dir)
 
# Load the VTK file
vtk_file_path = os.path.join('postProcessing/planes', str(max_d), 'alpha.wetting_xy.vtk')
mesh = pv.read(vtk_file_path)

# Create a plotter with better quality settings
plotter = pv.Plotter(off_screen=True)
plotter.set_background('white')  # Set background color to white

# Set the colorbar range to [0, 1] by directly modifying the scalars of the mesh
mesh['alpha.wetting'] = mesh['alpha.wetting'].clip(0, 1)


plotter.add_mesh(mesh, scalars='alpha.wetting', cmap='jet', show_edges=False)
plotter.add_title(f'Time: {max_d} s', font_size=10)
plotter.remove_scalar_bar()
fig_width = 960
fig_hight = 400
# Set a larger window size and higher resolution
plotter.window_size = (fig_width, fig_hight)  # Adjust the resolution as needed


# Adjust the camera to zoom and center the scene in XY view
plotter.camera_position = 'xy'
plotter.camera.zoom (2.5)

# Add the colorbar
colorbar = plotter.add_scalar_bar(title='Volume fraction', n_labels=5, shadow=False, width=0.5, label_font_size=16, title_font_size=18)

# Center the colormap horizontally
colorbar_position_x = 0.5 - colorbar.GetWidth() / 2
colorbar.SetDisplayPosition(int(colorbar_position_x * fig_width), int(0.01 * fig_hight))  # Adjust position as needed

# Capture the screenshot with the adjusted settings
png_file = f'alpha_{max_d}_xy.png'
plotter.show(screenshot=png_file)

# Optional: Export the scene to GLTF format if needed
# plotter.export_gltf('U_330.gltf')
