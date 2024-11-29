from realsense import realsense_model
from arena import Arena

import mujoco as mj
import mujoco.viewer



if __name__ =="__main__":


  arena = Arena()
  _,model = realsense_model("./realsense_d435i/assets/")

  arena.add_movable_asset(model,[0,0,0.23])
  model = arena.spec.compile()
  data = mj.MjData(model)

  print(arena.spec.to_xml())
  # visualization
  with mj.viewer.launch_passive(
        model=model, data=data, show_left_ui=False, show_right_ui=False
    ) as viewer:
        mj.mjv_defaultFreeCamera(model, viewer.cam)
        mj.mj_forward(model, data)
        while viewer.is_running():
            mj.mj_step(model, data)
            viewer.sync()
