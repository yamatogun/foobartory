#!/usr/bin/env/python3

'''
Single thread implementation
'''

import datetime
import sys
from collections import OrderedDict


class Foobartory:
    nfoo = 0  # TODO: read about class attributes
    nbar = 0
    nfoobar = 0

    schedule = OrderedDict()  # timestamps with corresponding robots

    def __init__(self, nrobots=2):
        for _ in range(nrobots):
            robot = Robot(start_time=datetime.datetime.now())
            self.register_robot(robot)

    def register_robot(self, robot):
        end_time = robot.end_time
        self.schedule.setdefault(end_time, [])
        self.schedule[end_time].append(robot)
        self.schedule = OrderedDict(
            sorted(self.schedule.items(), key=lambda x: x[0])
        )
        print(self.schedule)
        self.next_action_time = next(iter(self.schedule.items()))[0]

    def go(self):
        assert self.schedule, 'there should be at least one robot'
        while True:
            current_time = datetime.datetime.now()
            if current_time >= self.next_action_time:
                robots = self.schedule.popitem(last=False)[1]
                for robot in robots:
                    robot.work()

                    if self.nfoo >= 100:
                        sys.exit()

                    self.register_robot(robot)


class Robot:
    DURATIONS = {  # in seconds
        'mine_foo': 1,
    }

    robot_counter = 0

    def __init__(self, start_time):
        self.choose_task()
        self.start_time = start_time  # provided by factory

        self.name = self.robot_counter
        Robot.robot_counter += 1

    def __str__(self):
        return '<Robot {}>'.format(self.name)

    @property
    def end_time(self):
        assert self.current_task in self.DURATIONS
        task_duration = datetime.timedelta(
            seconds=self.DURATIONS[self.current_task]
        )
        return self.start_time + task_duration

    def choose_task(self):
        self.current_task = 'mine_foo'
        # TODO: to complete 

    def work(self):
        task = getattr(self, self.current_task)()
        self.choose_task()
        self.reinit_time()

    def reinit_time(self):
        self.start_time = datetime.datetime.now()

    def mine_foo(self):
        print('calling mine foo for:', self)
        Foobartory.nfoo += 1


if __name__ == '__main__':
    foobartory = Foobartory()
    foobartory.go()
