import numpy as np
import matplotlib.pyplot as plt

# Converted script w/ ChatGPT (GPT v3.5)

# Read simulation settings file
settingsfile = np.loadtxt('sim_params.csv', dtype=str, delimiter=' ')
Nbcn = 5000
Ntrg = 5000
spat_dims = 2

posfilename = ''
lincycles = 0
expcycles = 0
diffconst = 0

for i in range(0, len(settingsfile), 2):
    setting_key = settingsfile[i]
    setting_val = settingsfile[i+1]
    if setting_key == '-posfilename':
        posfilename = setting_val
    elif setting_key == '-lin_cycles':
        lincycles = float(setting_val)
    elif setting_key == '-exp_cycles':
        expcycles = float(setting_val)
    elif setting_key == '-diffconst':
        diffconst = float(setting_val)

sim_positions = np.zeros((Nbcn+Ntrg, 2+spat_dims))
sim_positions[Nbcn:Nbcn+Ntrg, 1] = 1  # indicate which are targets

im = plt.imread('im.tif')
im = im > 0
rows, cols = im.shape
xcoords, ycoords = np.zeros((rows, cols)), np.zeros((rows, cols))

for r in range(rows):
    for c in range(cols):
        if im[r, c] > 0:
            xcoords[r, c] = c
            ycoords[r, c] = -r

good_indices = np.where(xcoords > 0)
xcoords = xcoords[good_indices]
ycoords = ycoords[good_indices]
Npx = len(good_indices[0])

for n in range(Nbcn+Ntrg):
    sim_positions[n, 0] = n-1  # index from 0
    myrandindex = np.random.randint(0, Npx)
    sim_positions[n, 2] = xcoords[myrandindex] + (np.random.random() - 0.5)
    sim_positions[n, 3] = ycoords[myrandindex] + (np.random.random() - 0.5)

sim_positions[:, 2] -= np.mean(sim_positions[:, 2])
sim_positions[:, 3] -= np.mean(sim_positions[:, 3])

diff_lengthscale = np.sqrt(8 * 3 * diffconst * (lincycles + expcycles))
image_width = np.max(sim_positions[:, 2]) - np.min(sim_positions[:, 2])
sim_positions[:, 2:4] = sim_positions[:, 2:4] * (4 * diff_lengthscale / image_width)

np.savetxt(posfilename, sim_positions, delimiter=',')

myvars = np.var(sim_positions, axis=0)
print(np.sqrt(myvars[2:4]))

mycolors = plt.get_cmap('hsv')(np.linspace(0, 1, Nbcn+Ntrg))
colorcoords = np.zeros((Nbcn+Ntrg, 3))

min_x = np.min(sim_positions[:, 2])
max_x = np.max(sim_positions[:, 2])
min_y = np.min(sim_positions[:, 3])
max_y = np.max(sim_positions[:, 3])

totcolors = len(mycolors)
min_x -= 0.5
max_x += 0.5
min_y -= 0.5
max_y += 0.5

for n in range(Nbcn+Ntrg):
    colorcoords[n] = mycolors[int(((sim_positions[n, 2] - min_x) / (max_x + 0.1 - min_x)) * totcolors)]

sz = 10
plt.scatter(sim_positions[:, 2] / diff_lengthscale, sim_positions[:, 3] / diff_lengthscale, s=sz, c=colorcoords, marker='.')
plt.gca().set_xlim([np.floor(min_x / diff_lengthscale) - 1, np.ceil(max_x / diff_lengthscale) + 1])
plt.gca().set_ylim([np.floor(min_y / diff_lengthscale), np.ceil(max_y / diff_lengthscale)])
plt.gca().set_aspect('equal', adjustable='datalim')
plt.gca().tick_params(axis='both', labelsize=15, width=2)
plt.gca().spines['top'].set_linewidth(2)
plt.gca().spines['bottom'].set_linewidth(2)
plt.gca().spines['left'].set_linewidth(2)
plt.gca().spines['right'].set_linewidth(2)
plt.gca().set_facecolor('white')
plt.show()
