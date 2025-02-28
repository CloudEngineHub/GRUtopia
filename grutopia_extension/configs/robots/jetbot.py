from typing import Optional

from grutopia.core.config import RobotCfg
from grutopia.macros import gm
from grutopia_extension.configs.controllers import (
    DifferentialDriveControllerCfg,
    MoveAlongPathPointsControllerCfg,
    MoveToPointBySpeedControllerCfg,
)
from grutopia_extension.configs.sensors import CameraCfg

move_by_speed_cfg = DifferentialDriveControllerCfg(name='move_by_speed', wheel_base=0.1125, wheel_radius=0.03)

move_to_point_cfg = MoveToPointBySpeedControllerCfg(
    name='move_to_point',
    forward_speed=1.0,
    rotation_speed=1.0,
    threshold=0.1,
    sub_controllers=[move_by_speed_cfg],
)

move_along_path_cfg = MoveAlongPathPointsControllerCfg(
    name='move_along_path',
    forward_speed=1.0,
    rotation_speed=1.0,
    threshold=0.1,
    sub_controllers=[move_to_point_cfg],
)


camera = CameraCfg(
    name='camera',
    prim_path='chassis/rgb_camera/jetbot_camera',
    resolution=(640, 360),
)


class JetbotRobotCfg(RobotCfg):
    # meta info
    name: Optional[str] = 'jetbot'
    type: Optional[str] = 'JetbotRobot'
    prim_path: Optional[str] = '/World/jetbot'
    create_robot: Optional[bool] = True
    usd_path: Optional[str] = gm.ASSET_PATH + '/robots/jetbot/jetbot.usd'
