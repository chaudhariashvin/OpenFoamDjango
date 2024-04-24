import os

class ParametricOpenFoamCaseExecution:
     
    # Variables dependent on local OpenFOAM installation and server folder structure
    path_to_case_root = os.path.abspath('./OFCases')
    path_to_template_source = path_to_case_root + '/bio_2D_template'
    path_to_target = path_to_case_root + '/case'
   # path_to_U = path_to_target + '/0/U'
    path_to_setting = path_to_target + '/setUp'
   # path_to_geom = path_to_target + '/system/blockMeshDict'
   # path_to_VTK = path_to_target + '/VTK'
   # path_to_converged_VTK_solution_file = '' # to be updated after solution
   # path_to_gltf_3D_U = path_to_VTK + '/U.gltf'
   # path_to_gltf_3D_p = path_to_VTK + '/p.gltf'
   # path_to_U_png = path_to_VTK + '/U.png'
   # path_to_p_png = path_to_VTK + '/p.png'
    figure_width = 1200
    figure_height = 600

    def __init__(self, flow_rate_in=0.001, water_in=1, eps_top=0.4, eps_mid=0.34, eps_bot=0.4, ini_water_fraction=0.5, sim_end_time=300):
        
        # Variables dependent on user input
        self.flow_rate_in = flow_rate_in
        self.water_in = water_in
        self.eps_top = eps_top
        self.eps_mid = eps_mid
        self.eps_bot = eps_bot
        self.ini_water_fraction = ini_water_fraction
        self.sim_end_time = sim_end_time 
        
    def prepareFolder(self):
        from distutils.dir_util import copy_tree
        import shutil

        # Erase earlier case and results
        try:
            shutil.rmtree(ParametricOpenFoamCaseExecution.path_to_target)
            print(f"Folder '{ParametricOpenFoamCaseExecution.path_to_target}' and its contents have been removed successfully.")
        except OSError as e:
            print(f"Error: {e}")

        # Copy template folder
        #copy_tree(ParametricOpenFoamCaseExecution.path_to_template_source, ParametricOpenFoamCaseExecution.path_to_target)
        #print(f"THis is passed-1")

        import subprocess
        subprocess.run('cp -r bio_2D_template/ case', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_case_root,timeout=20)
        #print(f"THis is passed-2")

    def processFiles(self):
        
        # Geometry
        with open(ParametricOpenFoamCaseExecution.path_to_setting, 'r') as file:
            data = file.read()
        
        data = data.replace("REPLACEME_FLOWRATE", str(self.flow_rate_in))
        data = data.replace("REPLACEME_FLOWSIGN", str(self.water_in))
        data = data.replace("REPLACEME_POROSITY_1", str(self.eps_top))
        data = data.replace("REPLACEME_POROSITY_2", str(self.eps_mid))
        data = data.replace("REPLACEME_POROSITY_3", str(self.eps_bot))
        data = data.replace("REPLACEME_WATER_FRACTION", str(self.ini_water_fraction))
        data = data.replace("REPLACEME_END_TIME", str(self.sim_end_time))

        with open(ParametricOpenFoamCaseExecution.path_to_setting, "w") as file:
            file.write(data)
        

    def execFoam(self):
        import subprocess
        subprocess.run('blockMesh > log.blockMesh', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_target,timeout=50)
        subprocess.run('setFields > log.setField', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_target,timeout=50)
       ### subprocess.run('decomposePar > log.decompose', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_target,timeout=50)
      ###  subprocess.run('mpirun -np 8 --oversubscribe hybridPorousInterFoam -parallel > log.solver', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_target,timeout=3600)
        subprocess.run('hybridPorousInterFoam > log.solver', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_target,timeout=3600)
 
    def findConvergedSolutionFolder(self):
        # Finds the folder with highest integer number in the name (prouced by OpenFOAM as the converged sol'n)
        import os        
        intlistfolders = []
        list_subfolders_with_paths = [f.name for f in os.scandir(ParametricOpenFoamCaseExecution.path_to_target) if f.is_dir()]
        for x in list_subfolders_with_paths:
            try:
                intval = int(x)
                intlistfolders.append(intval)
            except:
                pass
        ParametricOpenFoamCaseExecution.path_to_converged_VTK_solution_file = ParametricOpenFoamCaseExecution.path_to_VTK + '/case_' + str(max(intlistfolders)) + '.vtk'

    def visualize_vtk(self, scalarField='U'):
        import pyvista as pv
        # Load the VTK file
        mesh = pv.read(ParametricOpenFoamCaseExecution.path_to_converged_VTK_solution_file)

        # Create a plotter and add the mesh with pressure data
        plotter = pv.Plotter(window_size=(ParametricOpenFoamCaseExecution.figure_width, ParametricOpenFoamCaseExecution.figure_height),off_screen=True)

        # Add the mesh to the plotter with the pressure data and colormap
        mesh_actor = plotter.add_mesh(mesh, scalars=scalarField, cmap='viridis', show_edges=False)

        # Customize the visualization settings
        plotter.set_background('white')

        # Reset the camera to zoom and center the scene
        plotter.reset_camera()

        # Remove the default colorbar
        plotter.remove_scalar_bar()
        
        # Add the colorbar to the plotter
        if scalarField == 'U':
            # Velocity magnitude
            label_txt = 'Velocity [m/s]'
            png_file = ParametricOpenFoamCaseExecution.path_to_U_png
            # Export the scene to GLTF format
            plotter.export_gltf(ParametricOpenFoamCaseExecution.path_to_gltf_3D_U)
        else:
            # Pressure
            label_txt = 'Pressure [Pa]'
            png_file = ParametricOpenFoamCaseExecution.path_to_p_png
            # Export the scene to GLTF format
            plotter.export_gltf(ParametricOpenFoamCaseExecution.path_to_gltf_3D_p)

        colorbar = plotter.add_scalar_bar(
            title='', n_labels=5, italic=False, shadow=False, width=0.5, above_label=label_txt
        )

        # Center the colormap horizontally
        colorbar_position_x = 0.5 - colorbar.GetWidth() / 2
        colorbar.SetDisplayPosition(int(colorbar_position_x*ParametricOpenFoamCaseExecution.figure_width), int(0.25*ParametricOpenFoamCaseExecution.figure_height))

        # Set view - this is a 2D model, so xy works
        plotter.camera_position = 'xy'

        # Do not display, but make a png file
        plotter.show(screenshot=png_file)


#OFC = ParametricOpenFoamCaseExecution()
#OFC.prepareFolder()
#OFC.processFiles()
#OFC.execFoam()
#OFC.findConvergedSolutionFolder()
#OFC.visualize_vtk(scalarField='U')
#OFC.visualize_vtk(scalarField='p')
jyki = 1

