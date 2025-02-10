from typing import Optional

from grutopia.core.config import RobotCfg
from grutopia_extension.configs.controllers import (
    AliengoMoveBySpeedControllerCfg,
    MoveAlongPathPointsControllerCfg,
    MoveToPointBySpeedControllerCfg,
    RotateControllerCfg,
)
from grutopia_extension.configs.sensors import CameraCfg

move_by_speed_cfg = AliengoMoveBySpeedControllerCfg(
    name='move_by_speed',
    policy_weights_path='GRUtopia/assets/robots/aliengo/policy/move_by_speed/aliengo_loco_model_4000.pt',
    joint_names=[
        'FL_hip_joint',
        'FR_hip_joint',
        'RL_hip_joint',
        'RR_hip_joint',
        'FL_thigh_joint',
        'FR_thigh_joint',
        'RL_thigh_joint',
        'RR_thigh_joint',
        'FL_calf_joint',
        'FR_calf_joint',
        'RL_calf_joint',
        'RR_calf_joint',
    ],
)

move_to_point_cfg = MoveToPointBySpeedControllerCfg(
    name='move_to_point',
    forward_speed=1.0,
    rotation_speed=4.0,
    threshold=0.05,
    sub_controllers=[move_by_speed_cfg],
)

move_along_path_cfg = MoveAlongPathPointsControllerCfg(
    name='move_along_path',
    forward_speed=1.0,
    rotation_speed=4.0,
    threshold=0.1,
    sub_controllers=[move_to_point_cfg],
)

rotate_cfg = RotateControllerCfg(
    name='rotate',
    rotation_speed=2.0,
    threshold=0.02,
    sub_controllers=[move_by_speed_cfg],
)

camera_cfg = CameraCfg(
    name='camera',
    prim_path='trunk/Camera',
)


class AliengoRobotCfg(RobotCfg):
    # meta info
    name: Optional[str] = 'aliengo'
    type: Optional[str] = 'AliengoRobot'
    prim_path: Optional[str] = '/World/aliengo'
    create_robot: Optional[bool] = True
    usd_path: Optional[str] = 'GRUtopia/assets/robots/aliengo/aliengo_camera.usdz'
