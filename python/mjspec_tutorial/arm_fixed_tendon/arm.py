import mujoco as mj

def arm_model():
  spec = mj.MjSpec()
  spec.compiler.degree = False
  model = spec.worldbody

  num_links = 3

  # defaults
  main = spec.default()
  main.joint.axis = [0,1,0]

  length = 0.2
  body = model
  for i in range(num_links):
    if i > 0:
      pos = [0, 0, (length+.03)]
    else:
      pos = [0]*3

    body = body.add_body(name="l"+str(i),pos = pos)
    body.add_geom(name="g1"+str(i),
                  type=mj.mjtGeom.mjGEOM_CYLINDER,
                  fromto = [0, .015, 0, 0, -.015, 0],
                  size = [.05,0,0],
                  rgba =[1.0, 0.5, 0.0, 1.0]
                  )
    body.add_geom(name= "g2"+str(i),
                  type= mj.mjtGeom.mjGEOM_CAPSULE,
                  fromto = [0]*5+[length],
                  size = [0.02,0,0],
                  rgba =[1,1,0,1]
                  )
    body.add_joint(name="j"+str(i),range=[-1,1])

  # creating tendon
  tendon = spec.add_tendon(name="tendon")
  # wrapping tendon around joints
  for i in range(num_links):
    joint = "j"+str(i)
    coef = 1
    tendon.wrap_joint(joint,coef)

  # actuation
  kp = 1
  main.actuator.gainprm[0] = kp
  main.actuator.biasprm[1] = -kp
  main.actuator.trntype = mj.mjtTrn.mjTRN_TENDON
  main.actuator.ctrlrange = [-1,1]
  spec.add_actuator(
    name="act_tendon", target="tendon"
  )

  return spec, model
