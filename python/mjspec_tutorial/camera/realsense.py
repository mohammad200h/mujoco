import mujoco as mj


def realsense_model(path:str):
  spec = mj.MjSpec()
  spec.compiler.degree = False
  model = spec.worldbody

  # defaults
  main = spec.default()
  main.material.specular = 0
  main.material.shininess = 0.25

  # visual default
  v_def = spec.add_default('visual', main)
  v_def.geom.group = 2
  v_def.geom.type = mj.mjtGeom.mjGEOM_MESH
  v_def.geom.contype = 0
  v_def.geom.conaffinity = 0
  v_def.geom.mass = 0

  # collision default
  c_def = spec.add_default('collision', main)
  c_def.geom.group =3
  c_def.geom.type = mj.mjtGeom.mjGEOM_MESH
  c_def.geom.mass = 0

  materials = {
    "Black_Acrylic":[0.070360, 0.070360, 0.070360, 1],
    "Cameras_Gray":[0.296138, 0.296138, 0.296138, 1],
    "IR_Emitter_Lens":[0.287440, 0.665387, 0.327778, 1],
    "IR_Lens":[0.035601, 0.035601, 0.035601, 1],
    "IR_Rim":[0.799102, 0.806952, 0.799103, 1],
    "Metal_Casing":[1, 1, 1, 1],
    "RGB_Pupil":[0.087140, 0.002866, 0.009346, 1]
  }
  for name,rgba in materials.items():
    spec.add_material(name=name,rgba=rgba)

  for i in range(9):
    spec.add_mesh(name="d435i_"+str(i),
                  file=path+"d435i_"+str(i)+".obj")
  body = model.add_body(name="d435i")

  #visual geoms
  materials_order = ["IR_Lens","IR_Emitter_Lens",
                     "IR_Rim","IR_Lens","Cameras_Gray","Black_Acrylic",
                     "Black_Acrylic","RGB_Pupil"
                     ]
  for i,material in enumerate(materials_order):
    body.add_geom(default = v_def,
                  meshname="d435i_"+str(i),
                  material=material
                  )
  body.add_geom(
    default = v_def,
    meshname="d435i_8",
    material="Metal_Casing",
    mass=0.072
  )
  # collision geom
  body.add_geom(default = c_def,
                type=mj.mjtGeom.mjGEOM_CAPSULE,
                meshname="d435i_8"
                )

  return spec,model
