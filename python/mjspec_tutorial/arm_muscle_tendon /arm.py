import mujoco as mj

def arm_model():
  spec = mj.MjSpec()
  spec.compiler.degree = False
  model = spec.worldbody

  num_links = 3

  # defaults
  main = spec.default()
  main.joint.axis = [0,1,0]
  # muscle defaults
  main.actuator.trntype = mj.mjtTrn.mjTRN_TENDON
  main.actuator.dyntype  = mj.mjtDyn.mjDYN_MUSCLE
  main.actuator.gaintype = mj.mjtGain.mjGAIN_MUSCLE
  main.actuator.biastype = mj.mjtBias.mjBIAS_MUSCLE
  main.actuator.dynprm[0] = 0.01 # tau act
  main.actuator.dynprm[1] = 0.04 # tau deact
  # range[0], range [1], force, scale,
  # lmin, lmax, vmax, fpmax, fvmax
  main.actuator.gainprm[0:9] = [0.75,1.05,-1,200,
                                0.5,1.6,1.5,1.3,1.2]
  # biasprm = gainprm
  main.actuator.biasprm = main.actuator.gainprm[:]

  length = 0.2
  body = model
  for i in range(num_links):
    if i > 0:
      pos = [0, 0, (length+.03)]
    else:
      pos = [0]*3

    temp_b = body.add_body(name="l"+str(i),pos = pos)
    temp_b.add_geom(name="g1"+str(i),
                  type=mj.mjtGeom.mjGEOM_CYLINDER,
                  fromto = [0, .015, 0, 0, -.015, 0],
                  size = [.05,0,0],
                  rgba =[1.0, 0.5, 0.0, 1.0]
                  )
    temp_b.add_geom(name= "g2"+str(i),
                  type= mj.mjtGeom.mjGEOM_CAPSULE,
                  fromto = [0]*5+[length],
                  size = [0.02,0,0],
                  rgba =[1,1,0,1]
                  )
    temp_b.add_joint(name="j"+str(i),range=[-1,1])

    # tendon routing
    for j in range(2):
      sign = (-1)**j
      p_z = 0.15
      if i==0:
        p_z = -0.08
      # sites on parent
      body.add_site(
        name="p"+str(i)+str(j),
        pos=[sign *0.025,0,p_z]
      )
      # sidesites
      temp_b.add_site(
        name="ch_ss"+str(i)+str(j),
        pos = [sign *0.08,0,0]
      )
      # sites on child
      temp_b.add_site(
        name="ch"+str(i)+str(j),
        pos = [sign * 0.025,0,0.08]
      )
      # tendon routing
      t = spec.add_tendon(name="t"+str(i)+str(j))
      t.wrap_site("p"+str(i)+str(j))
      t.wrap_geom("g1"+str(i),"ch_ss"+str(i)+str(j))
      t.wrap_site("ch"+str(i)+str(j))
      # muscle
      spec.add_actuator(name="act"+str(i)+str(j),
                        target = "t"+str(i)+str(j)
                        )
    body = temp_b

  return spec, model
