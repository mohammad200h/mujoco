
import mujoco as mj

import matplotlib.pyplot as plt
import numpy as np
from perlin_numpy import (
    generate_perlin_noise_2d, generate_fractal_noise_2d
)
def demo():

  np.random.seed(0)
  noise = generate_perlin_noise_2d((256, 256), (8, 8))
  plt.imshow(noise, cmap='gray', interpolation='lanczos')
  plt.colorbar()

  np.random.seed(0)
  noise = generate_fractal_noise_2d((256, 256), (8, 8), 5)
  plt.figure()
  plt.imshow(noise, cmap='gray', interpolation='lanczos')
  plt.colorbar()
  plt.show()

class Hfield:
  def __init__(self):
    self.spec = mj.MjSpec()
    self.model = self.spec.worldbody

    self.spec.compiler.degree = False

    noise = generate_perlin_noise_2d((256, 256), (8, 8))

    self.spec.add_hfield(userdata=noise)
