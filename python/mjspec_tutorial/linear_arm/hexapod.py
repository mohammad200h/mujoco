import mujoco as mj
import numpy as np
from linear_arm import linear_arm_model

def make_hexapod(equality3 = False,equality2 = False,
                 exclude_contact = False):
  spec = mj.MjSpec()
  spec.compiler.degree = False
  model = spec.worldbody
  _,arm_model = linear_arm_model()

  l_arm,r_arm = 0.1 , 0.03
  radius = 0.1

  #base
  base = model.add_body(name="base")
  base.add_geom(size=[radius]*2+[radius/2],
                type = mj.mjtGeom.mjGEOM_ELLIPSOID
                )
  arms = []
  for i in range(3):
    theta = 2 * i * np.pi / 3
    pos = radius * np.array([np.cos(theta), np.sin(theta), 0])
    frame = base.add_frame(pos = pos,euler = [0,0,theta])
    arm = frame.attach_body(arm_model,"arm" + str(i), '')
    arms.append(arm)


  top = None
  if equality3:
    # creating top panel
    top = model.add_body(name="top",pos=[0,0,(l_arm+r_arm)*2])
    top.add_geom(size=[radius]*2+[radius/2],
                type = mj.mjtGeom.mjGEOM_ELLIPSOID
                )
    # adding sites to top panel
    # and adding equality constraints
    for i in range(3):
      theta = 2 * i * np.pi / 3
      site_pos = radius * np.array([np.cos(theta), np.sin(theta), 0])
      top_site = top.add_site(pos=site_pos,name="top_site"+str(i),
                              euler=[0,0,theta])
      l2 = arms[i].bodies[0].bodies[0]
      l2_site = l2.sites[0]
      spec.add_equality(objtype=mj.mjtObj.mjOBJ_SITE,
                        name1=top_site.name,
                        name2=l2_site.name
                        )

  if equality2:
    arm_0_l1 = arms[0].bodies[0].bodies[0]
    print(f"arm_0_l1::name::{arm_0_l1.name}")
    top = arm_0_l1.add_body(name="top",pos=[-radius,0,2*(l_arm)+r_arm])
    top.add_geom(size=[radius]*2+[radius/2],
                type = mj.mjtGeom.mjGEOM_ELLIPSOID
                )
    top.add_joint(
      type = mj.mjtJoint.mjJNT_BALL,
      pos = [radius,0,0]
    )
    # adding sites to top panel
    # and adding equality constraints
    for i in range(1,3):
      theta = 2 * i * np.pi / 3
      site_pos = radius * np.array([np.cos(theta), np.sin(theta), 0])
      top_site = top.add_site(pos=site_pos,name="top_site"+str(i),
                              euler=[0,0,theta])
      l2 = arms[i].bodies[0].bodies[0]
      l2_site = l2.sites[0]
      spec.add_equality(objtype=mj.mjtObj.mjOBJ_SITE,
                        name1=top_site.name,
                        name2=l2_site.name
                        )

  if exclude_contact:
    for i in range(3):
      l0 = arms[i].bodies[0]
      l1 = l0.bodies[0]
      # removing contact between l0 or l1 with base
      spec.add_exclude(bodyname1=base.name,bodyname2=l0.name)
      spec.add_exclude(bodyname1=base.name,bodyname2=l1.name)
      # removing contact between l1 and top
      spec.add_exclude(bodyname1=top.name,bodyname2=l1.name)


  return spec, model