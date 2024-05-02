import numpy as np
import matplotlib.pyplot as plt
import os

# List available time directories
#dir = os.listdir('postProcessing/planes')
#dir = [int(value) for value in dir]

# Find the maximum time directory
#max_d = max(dir)

# Read data from files
def read_data(file_path):
    data = np.genfromtxt(file_path, delimiter='\t', skip_header=4)
    return data

big = read_data('postProcessing/big_out/0/surfaceFieldValue.dat')
lower = read_data('postProcessing/lower_out/0/surfaceFieldValue.dat')
upper = read_data('postProcessing/upper_out/0/surfaceFieldValue.dat')
inlet = read_data('postProcessing/inlet_flow/0/surfaceFieldValue.dat')
vol = read_data('postProcessing/waterVolume/0/volFieldValue.dat')

big [:, 2]= big[:, 2]+upper[:, 2];
# Plot the data
plt.figure()

# Plot the inlet flow rate
plt.plot(inlet[:, 0], -inlet[:, 2] * 1000, '.', linewidth=1, markersize=8, label='Inflow')

# Plot the infiltrate flow rate
plt.plot(lower[:, 0], lower[:, 2] * 1000, '.', linewidth=1, markersize=8, label='Infiltrate')
##plt.plot(upper[:, 0], upper[:, 2] * 1000, '.', linewidth=1, markersize=8, label='Overflow_small')

# Plot the overflow flow rate
plt.plot(big[:, 0], abs(big[:, 2]) * 1000, '.', linewidth=1, markersize=8, label='Overflow')


t=vol[:, 0]

# Find the maximum time 
max_t = int(max(t))

plt.grid(True)
f_title = f'Time:{max_t} s'
plt.title(f_title,fontsize=14)
plt.legend(['Inflow', 'Outlet-pipe', 'Runoff'],fontsize=12)
plt.ylabel('Flow rate [l/s]',fontsize=12)
plt.xlabel('Time [s]',fontsize=12)

# Set plot properties
#plt.gca().set_linewidth(1)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Save the figure as a PNG file
png_file = f'graph_{max_t}_xy.png'
plt.gcf().set_size_inches(8, 3.2)
plt.savefig(png_file, dpi=100, bbox_inches='tight')

# Show the plot (optional)
# plt.show()

