from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
import glob
from OFapp.utils.ParametricOpenFoamCaseExecution import ParametricOpenFoamCaseExecution
from django.conf import settings
import shutil
import subprocess
from functools import cmp_to_key

def ResolveOpenFOAM(_flow_rate_in, _water_in, _eps_top, _eps_mid, _eps_bot, _ini_water_fraction, _sim_end_time):
    filename1 = ''
    filename2 = ''
    OFC = ParametricOpenFoamCaseExecution(flow_rate_in=_flow_rate_in,water_in=_water_in,eps_top=_eps_top,eps_mid=_eps_mid,eps_bot=_eps_bot,ini_water_fraction=_ini_water_fraction, sim_end_time=_sim_end_time)
    OFC.prepareFolder()
    OFC.processFiles()
    OFC.execFoam()
 #   OFC.findConvergedSolutionFolder()
 #   OFC.visualize_vtk(scalarField='U')
 #   OFC.visualize_vtk(scalarField='p')
    
    # Iteration count 
    itrs_string = OFC.path_to_converged_VTK_solution_file.split('_')[-1].split('.vtk')[0]

    # Copy the files
    source_path_to_U_png = ParametricOpenFoamCaseExecution.path_to_U_png
    source_path_to_p_png = ParametricOpenFoamCaseExecution.path_to_p_png

    # Define the destination paths in the media folder
    destination_path_to_U_png = os.path.join(settings.MEDIA_ROOT, itrs_string + '_U.png')
    destination_path_to_p_png = os.path.join(settings.MEDIA_ROOT, itrs_string + '_p.png')

    # Copy the PNG files to the media folder
    shutil.copy(source_path_to_U_png, destination_path_to_U_png)
    shutil.copy(source_path_to_p_png, destination_path_to_p_png)

    # Get the relative paths to the images (relative to MEDIA_ROOT)
    relative_path_to_U_png = os.path.relpath(destination_path_to_U_png, start=settings.BASE_DIR)
    relative_path_to_p_png = os.path.relpath(destination_path_to_p_png, start=settings.BASE_DIR)

    return relative_path_to_U_png, relative_path_to_p_png
    

def input_form_view(request):
    context = {}  # Create a dictionary to hold context data
    
    if request.method == 'POST':
        subprocess.run('rm -f ./media/*.png', shell=True, timeout=20)

        flow_rate_in = request.POST.get('flow_rate_in')
        water_in = request.POST.get('water_in')
        eps_top = request.POST.get('eps_top')
        eps_mid = request.POST.get('eps_mid')
        eps_bot = request.POST.get('eps_bot')
        ini_water_fraction = request.POST.get('ini_water_fraction')
        sim_time_end = request.POST.get('sim_time_end')

        # Validate inputs
        if all(val is not None and val.strip() != '' for val in [flow_rate_in, water_in, eps_top, eps_mid, eps_bot, ini_water_fraction, sim_time_end]):
            try:
                flow_rate_in = float(flow_rate_in)
                water_in = float(water_in)
                eps_top = float(eps_top)
                eps_mid = float(eps_mid)
                eps_bot = float(eps_bot)
                ini_water_fraction = float(ini_water_fraction)
                sim_time_end = float(sim_time_end)

                # Set previous input values in the context to pre-populate the form
                context['previous_input'] = {
                    'flow_rate_in': flow_rate_in,
                    'water_in': water_in,
                    'eps_top': eps_top,
                    'eps_mid': eps_mid,
                    'eps_bot': eps_bot,
                    'ini_water_fraction': ini_water_fraction,
                    'sim_time_end': sim_time_end,
                }
                
                # Check validity conditions
                if 0 < flow_rate_in < 1 and -1 < water_in < 1.1 and 0 < eps_top < 1 and 0 < eps_mid < 1 and 0 < eps_bot < 1 and 0 < ini_water_fraction < 1 and 0 < sim_time_end < 360000:
                    # Call your custom Python function here, passing the inputs as arguments
                    figure1_filename, figure2_filename = ResolveOpenFOAM(flow_rate_in, water_in, eps_top, eps_mid, eps_bot, ini_water_fraction, sim_time_end)

                    # Add the filenames to the context to be used in the template
                    context['figure1_filename'] = figure1_filename
                    context['figure2_filename'] = figure2_filename

                    # You can return the result to the user or do anything else you want with it
                    # return HttpResponse(f"Result: Check the figures below.")
                    # return render(request, 'case_inputs.html', context)
                
                else:
                    # Set an error message in the context
                    context['error_message'] = "Invalid input. Please ensure U and the dx, dy values satisfy the conditions."
            except ValueError:
                # Set an error message in the context
                context['error_message'] = "Invalid input. Please enter valid numbers."

        else:
            # Set an error message in the context
            context['error_message'] = "Please fill in all the input fields."
        return JsonResponse(context)
    else:
        # Define your default values here
        context['previous_input'] = {
                    'flow_rate_in': 0.005,
                    'water_in': 1,
                    'eps_top': 0.4,
                    'eps_mid': 0.34,
                    'eps_bot': 0.4,
                    'ini_water_fraction': 0.5,
                    'sim_time_end': 300,
        }
        
    # Pass the context to the template
    print(context)
    return render(request, 'case_inputs.html', context)

 
def get_intermediate_images(request):
    if request.method == 'GET':
        subprocess.run('cp -r case/*.png ../media', shell=True, cwd=ParametricOpenFoamCaseExecution.path_to_case_root,timeout=20)
        lf_1 = glob.glob("media/alpha_*.png")
        lf_2 = glob.glob("media/graph_*.png")
        lf_1 = sorted(lf_1,  key=cmp_to_key(lambda x, y: int(x.split("_")[1]) - int(y.split("_")[1])))
        lf_2 = sorted(lf_2,  key=cmp_to_key(lambda x, y: int(x.split("_")[1]) - int(y.split("_")[1])))

        latest_1 = "" if len(lf_1) == 0 else lf_1[-1]
        latest_2 = "" if len(lf_2) == 0 else lf_2[-1]

        #print(lf)
        #print(latest)
        res = {
           # "files_1": lf_1,
            "latest_1": latest_1,
           # "files_2": lf_2,
            "latest_2": latest_2
        }
        return JsonResponse(res)
