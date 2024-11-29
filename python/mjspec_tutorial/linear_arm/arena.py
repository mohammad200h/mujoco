import mujoco as mj


class Arena:
  def __init__(self):
    self.spec = mj.MjSpec()
    self.model = self.spec.worldbody

    self.spec.compiler.degree = False
    self.robots = []

    # Make arena with textured floor.
    chequered = self.spec.add_texture(
        name="chequered", type=mj.mjtTexture.mjTEXTURE_2D,
        builtin=mj.mjtBuiltin.mjBUILTIN_CHECKER,
        width=300, height=300, rgb1=[.2, .3, .4], rgb2=[.3, .4, .5])
    grid = self.spec.add_material(
        name='grid', texrepeat=[5, 5], reflectance=.2
        ).textures[mj.mjtTextureRole.mjTEXROLE_RGB] = 'chequered'
    self.model.add_geom(
        type=mj.mjtGeom.mjGEOM_PLANE, size=[2, 2, .1], material='grid')
    for x in [-2, 2]:
      self.model.add_light(pos=[x, -1, 3], dir=[-x, 1, -2])

  def add_robot(self,model,pos=[0,0,0],prefix='_'):
    frame = self.model.add_frame(pos=pos)
    body = frame.attach_body(model,  prefix,'')
    body.add_freejoint()

  def add_fixed_robot(self,model,pos=[0,0,0],prefix='_'):
    self.robots.append(model)
    frame = self.model.add_frame(pos=pos)
    body = frame.attach_body(model,  prefix,'')
