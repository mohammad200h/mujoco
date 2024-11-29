import mujoco as mj

def leg_model():
  spec = mj.MjSpec()
  spec.compiler.degree = False

  spec.add_material(name = "yellow",rgba = [1,1,0,1])

  # defaults for joint and geom
  main = spec.default()
  main.joint.damping = 10
  main.geom.material = "yellow"
  main.geom.type = mj.mjtGeom.mjGEOM_CAPSULE
  main.geom.mass = 1

  model = spec.worldbody
  body = model
  angle, length, radius = 0, 0.1, 0.03
  fromto = [
    [0]*3+[length]+[0]*2,
    [0]*5+[-length]
  ]
  # tree
  j_axis = [[0,0,1],[0,1,0]]
  for i in range(2):
    body = body.add_body(name = "l"+str(i),pos = [length*i,0,0])
    body.add_geom(fromto = fromto[i],size = [length/4,0,0])
    body.add_joint(name="j"+str(i),axis=j_axis[i])
  body.add_site(name="feet",pos=[0,0,-(length + radius)])

  # defaults for position actuation
  kp = 10
  main.actuator.trntype = mj.mjtTrn.mjTRN_JOINT
  main.actuator.gaintype = mj.mjtGain.mjGAIN_FIXED
  main.actuator.biastype = mj.mjtBias.mjBIAS_AFFINE
  main.actuator.gainprm[0] =  kp
  main.actuator.biasprm[1] = -kp

  # actuators
  for i in range(2):
    spec.add_actuator(name = "act" + str(i),
                       target = "j" + str(i))
  # joint sensor
  spec.add_sensor(name = "j0_sensor",
                  objname = "j0",
                  type = mj.mjtSensor.mjSENS_JOINTPOS,
                  objtype = mj.mjtObj.mjOBJ_JOINT
                )
  # force sensor
  spec.add_sensor(name = "force_sensor",
                  objname = "feet",
                  type = mj.mjtSensor.mjSENS_FORCE,
                  objtype = mj.mjtObj.mjOBJ_SITE
                )

  return spec, model