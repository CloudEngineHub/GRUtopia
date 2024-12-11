from typing import Any

import gymnasium as gym

import grutopia.core.util.space as space
from grutopia.core.config import ValidatedConfig
from grutopia.core.runtime import SimulatorRuntime


class Env(gym.Env):
    """
    Gym Env for a single environment with a single learning agent.
    ----------------------------------------------------------------------
    """
    RESET_INFO_TASK_RUNTIME = 'task_runtime'

    def __init__(self, simulator_runtime: SimulatorRuntime) -> None:
        self._render = None
        self._runtime = simulator_runtime
        self._robot_name = None
        self._current_task_name = None
        self.action_space = self._get_action_space()
        self.observation_space = self._get_observation_space()
        self._validate()

        from grutopia.core.runner import SimulatorRunner  # noqa E402.

        self._runner = SimulatorRunner(simulator_runtime=simulator_runtime)

        return

    def _validate(self):
        if self._runtime.env_num > 1:
            raise ValueError(f'Only support single env now, but env num is {self._runtime.env_num}')

        robot_name = None
        config = ValidatedConfig(**self._runtime.config)
        for episode in config.task_config.episodes:
            if len(episode.robots) != 1:
                raise ValueError(f'Only support single agent now, but episode requires {len(episode.robots)} agents')
            if robot_name is None:
                robot_name = episode.robots[0].name
            else:
                if robot_name != episode.robots[0].name:
                    raise ValueError('Only support single agent now, but episode requires multiple agents')

        self._robot_name = f'{robot_name}_{0}'

    def _get_action_space(self) -> gym.Space:
        return space.get_action_space_by_task(self._runtime.config['task_config']['type'])

    def _get_observation_space(self) -> gym.Space:
        return space.get_observation_space_by_task(self._runtime.config['task_config']['type'])

    def reset(self, *, seed=None, options=None) -> tuple[gym.Space, dict[str, Any]]:
        """Resets the environment to an initial internal state, returning an initial observation and info.

        Args:
            seed (optional int): The seed that is used to initialize the environment's PRNG (`np_random`).
            options (optional dict): Additional information to specify how the environment is reset (optional,
                depending on the specific environment)

        Returns:
            observation (ObsType): Observation of the initial state.
            info (dictionary):  Contains the key `task_runtime` if there is an unfinished task
        """
        obs = {}
        info = {}

        origin_obs, task_runtime = self.runner.reset(self._current_task_name)
        if task_runtime is not None:
            self._current_task_name = task_runtime.name
            info[Env.RESET_INFO_TASK_RUNTIME] = task_runtime
            obs = origin_obs[task_runtime.name][self._robot_name]

        return obs, info

    def step(self, action: gym.Space) -> tuple[gym.Space, float, bool, bool, dict[str, Any]]:
        """
        run step with given action(with isaac step)


        Args:
            action (gym.Space): an action provided by the agent to update the environment state.

        Returns:
            observation (gym.Space): An element of the environment's :attr:`observation_space` as the next observation due to the agent actions.

            reward (float): The reward as a result of taking the action.
            terminated (bool): Whether the agent reaches the terminal state. If true, the user needs to call :meth:`reset`.
            truncated (bool): Whether the truncation condition outside the scope of the MDP is satisfied.
                Typically, this is a timelimit, but could also be used to indicate an agent physically going out of bounds.
                Can be used to end the episode prematurely before a terminal state is reached.
                If true, the user needs to call :meth:`reset`.
            info (dict): Contains auxiliary diagnostic information (helpful for debugging, learning, and logging).
                Currently it contains nothing.
        """

        obs = {}
        reward = 0.0
        terminated = True
        truncated = False
        info = {}

        if self._current_task_name is None:
            return obs, reward, terminated, truncated, info

        _actions = {self._current_task_name: {self._robot_name: action}}
        origin_obs, terminated_status = self._runner.step(_actions)

        obs = origin_obs[self._current_task_name][self._robot_name]
        terminated = terminated_status[self._current_task_name]

        return obs, reward, terminated, truncated, info

    @property
    def runner(self):
        return self._runner

    @property
    def is_render(self):
        return self._render

    @property
    def active_runtimes(self):
        return self.runtime.active_runtime()

    def get_dt(self):
        """
        Get dt of simulation environment.
        Returns:
            dt.
        """
        return self._runner.dt

    def get_observations(self) -> gym.Space:
        """
        Get observations from Isaac environment

        Returns:
            observation (gym.Space): observation
        """
        if self._current_task_name is None:
            return {}

        _obs = self._runner.get_obs()
        return _obs[self._current_task_name][self._robot_name]

    def render(self, mode='human'):
        pass

    def close(self):
        """close the environment"""
        self._runtime.simulation_app.close()
        return

    @property
    def simulation_runtime(self):
        """config of simulation environment"""
        return self._runtime.active_runtime()

    @property
    def simulation_app(self):
        """simulation app instance"""
        return self._runtime.simulation_app

    def finished(self) -> bool:
        """check if all tasks are finished"""
        return len(self._runner.current_tasks) == 0
