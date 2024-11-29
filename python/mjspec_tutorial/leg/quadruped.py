from leg import leg_model
import mujoco as mj
import numpy as np

def quadruped_model():
  spec = mj.MjSpec()
  spec.compiler.degree = False
  spec.add_material(name = "yellow",rgba = [1,1,0,1])

  model = spec.worldbody
  _, l_model = leg_model()

  body = model.add_body(name="torso")

  radius = 0.1
  body.add_geom(size=[radius]*2+[radius/2],
                material = "yellow",
                type = mj.mjtGeom.mjGEOM_ELLIPSOID
                )
  #legs
  for i in range(4):
    theta = 2 * i * np.pi / 4
    hip_pos = radius * np.array([np.cos(theta), np.sin(theta), 0])
    frame = body.add_frame(pos = hip_pos,euler = [0,0,theta])
    frame.attach_body(l_model, '', 'leg' + str(i))

  return spec,model
