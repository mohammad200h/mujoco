import mujoco as mj

def linear_arm_model():
  spec = mj.MjSpec()
  spec.compiler.degree = False

  main = spec.default()
  main.geom.type = mj.mjtGeom.mjGEOM_CAPSULE
  main.geom.mass = 1

  kp = 200
  main.actuator.trntype = mj.mjtTrn.mjTRN_JOINT
  main.actuator.gaintype = mj.mjtGain.mjGAIN_FIXED
  main.actuator.biastype = mj.mjtBias.mjBIAS_AFFINE
  main.actuator.gainprm[0] =  kp
  main.actuator.biasprm[1] = -kp


  model = spec.worldbody
  body = model
  length, radius = 0.1, 0.03
  fromto = [[0]*5+[length], [0]*5+[length*2]]
  rgba = [[1,1,0,1], [1.0, 0.5, 0.0, 1.0]]
  j_axis = [[1,0,0],[0,0,1]]
  j_type = [mj.mjtJoint.mjJNT_HINGE, mj.mjtJoint.mjJNT_SLIDE]
  j_range = [[-1,1],[0,0.05]]
  for i in range(2):
    body = body.add_body(name = "l"+str(i),pos = [0,0,length/2*i])
    body.add_geom(fromto = fromto[i],
                  size = [radius+(1e-4)*i,0,0],
                  rgba = rgba[i]
                  )
    body.add_joint(name = "j"+str(i),
                   axis = j_axis[i],
                   type = j_type[i],
                   range = j_range[i]
                   )
  body.add_site(name="arm_site",pos=[0,0,length*2+radius])
  spec.add_actuator(name="act",target="j1")

  return spec, model
