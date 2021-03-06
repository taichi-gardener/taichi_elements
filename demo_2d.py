import taichi as ti
import numpy as np
from mpm_solver import MPMSolver

write_to_disk = False

ti.init(arch=ti.cuda) # Try to run on GPU

gui = ti.GUI("Taichi MLS-MPM-99", res=512, background_color=0x112F41)

mpm = MPMSolver(res=(128, 128))

for i in range(3):
  mpm.add_cube(lower_corner=[0.2 + i * 0.1, 0.3 + i * 0.1], cube_size=[0.1, 0.1], material=MPMSolver.material_elastic)

for frame in range(500):
  mpm.step(8e-3)
  if 10 < frame < 100 and frame % 2 == 0:
    mpm.add_cube(lower_corner=[0.4, 0.7], cube_size=[0.2, 0.01], material=MPMSolver.material_water)
  if 120 < frame < 300 and frame % 40 == 0:
    mpm.add_cube(lower_corner=[0.4 + frame * 0.001, 0.6 + frame // 40 * 0.02], cube_size=[0.2, 0.1], material=MPMSolver.material_snow)
  colors = np.array([0x068587, 0xED553B, 0xEEEEF0], dtype=np.uint32)
  np_x, np_v, np_material = mpm.particle_info()
  gui.circles(np_x, radius=1.5, color=colors[np_material])
  gui.show(f'{frame:06d}.png' if write_to_disk else None)
