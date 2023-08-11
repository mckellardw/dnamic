import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import random

# Read in simulation settings file
settingsfile = pd.read_csv(
    'sim_params.csv', 
    delimiter=' ', 
    header=None
).values.flatten()
Nbcn = 5000
Ntrg = 5000
spat_dims = 2

# Parse settings file
for i in range(0, len(settingsfile), 2):
    setting_key = settingsfile[i]
    setting_val = settingsfile[i+1]
    if setting_key == '-posfilename':
        posfilename = setting_val
    elif setting_key == '-lin_cycles':
        lincycles = int(setting_val)
    elif setting_key == '-exp_cycles':
        expcycles = int(setting_val)
    elif setting_key == '-diffconst':
        diffconst = float(setting_val)

# Initialize sim_positions
sim_positions = np.zeros((Nbcn+Ntrg, 2+spat_dims))
sim_positions[Nbcn:(Nbcn+Ntrg), 1] = 1  # indicate which are targets

# Read image and get coordinates
im = np.array(Image.open('im.tif'))
im = (im > 0)
rows, cols = im.shape
xcoords = np.zeros((rows, cols))
ycoords = np.zeros((rows, cols))

for r in range(rows):
    for c in range(cols):
        if im[r, c] > 0:
            xcoords[r, c] = c
            ycoords[r, c] = -r

# Get good indices
good_indices = np.nonzero(xcoords.flatten() > 0)[0]
xcoords = xcoords.flatten()[good_indices]
ycoords = ycoords.flatten()[good_indices]
Npx = len(good_indices)

# Fill sim_positions
for n in range(Nbcn+Ntrg):
    sim_positions[n, 0] = n  # index from 0
    myrandindex = random.randint(0, Npx-1)
    sim_positions[n, 2] = xcoords[myrandindex] + (random.random()-0.5)
    sim_positions[n, 3] = ycoords[myrandindex] + (random.random()-0.5)

# Normalize sim_positions
sim_positions[:, 2] -= np.mean(sim_positions[:, 2])
sim_positions[:, 3] -= np.mean(sim_positions[:, 3])

# Calculate diff_lengthscale and image_width
diff_lengthscale = np.sqrt(8*3*diffconst*(lincycles + expcycles))
image_width = np.max(sim_positions[:, 2])-np.min(sim_positions[:, 2])
sim_positions[:, [2, 3]] *= (4*diff_lengthscale/image_width)  # arbitrary: set to simulate reasonable point spacings for simulation

# Write to csv
np.savetxt(posfilename, sim_positions, delimiter=',')

# Print sqrt of variances
print(np.sqrt(np.var(sim_positions[:, 2:4], axis=0)))

# Plotting
mycolors = plt.get_cmap('hsv')
colorcoords = np.zeros((Nbcn+Ntrg, 3))
min_x = np.min(sim_positions[:, 2])
max_x = np.max(sim_positions[:, 2])
min_y = np.min(sim_positions[:, 3])
max_y = np.max(sim_positions[:, 3])
totcolors = mycolors.N
min_x -= 0.5
max_x += 0.5
min_y -= 0.5
max_y += 0.5

for n in range(Nbcn+Ntrg):
    colorcoords[n, :] = mycolors(int(((sim_positions[n, 2]-min_x)/(max_x+0.1-min_x))*totcolors))[:3]

plt.scatter(
    sim_positions[:, 2]/diff_lengthscale, 
    sim_positions[:, 3]/diff_lengthscale, 
    s=10, 
    c=colorcoords
)
plt.gca().set_xlim(
    [np.floor(min_x/diff_lengthscale)-1, np.ceil(max_x/diff_lengthscale)+1]
)
plt.gca().set_ylim(
    [np.floor(min_y/diff_lengthscale), np.ceil(max_y/diff_lengthscale)]
)
plt.gca().tick_params(
    axis='both', 
    which='major', 
    labelsize=15
)
plt.gca().spines['left'].set_linewidth(2)
plt.gca().spines['bottom'].set_linewidth(2)
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('posfile.png')
plt.show()
