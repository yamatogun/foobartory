#!/usr/bin/env/python3

'''
Single thread implementation
'''

import datetime
import sys


def get_time_with_tens_of_seconds_precision(dt):
    '''
    <dt> is a datetime.datetime object
    '''
    def round_microseconds(microseconds):
        return (round(microseconds / 10**5)) * 10**5

    rounded_time = datetime.datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
        microsecond=0,
    ) + datetime.timedelta(microseconds=round_microseconds(dt.microsecond))
    return rounded_time


class Foobartory:
    nfoo = 0  # TODO: read about class attributes
    nbar = 0
    nfoobar = 0

    elapsed_time = 0
    robots = []

    def __init__(self, nrobots=2):
        for _ in range(nrobots):
            self.robots.append(Robot(self.elapsed_time))

    def go(self):
        while True:
            time.sleep(.5)
            for robot in self.robots:
                robot.update()
                print('nfoo: ', self.nfoo)

                if self.nfoo >= 100:
                    sys.exit()


class Robot:
    TIME_PER_TASK = {
        'mine_foo': 1,
    }

    robot_counter = 0

    def __init__(self, start_time):
        self.start_time = self.current_time = start_time  # provided by factory

        self.name = self.robot_counter
        Robot.robot_counter += 1

        self.choose_task()

    def __str__(self):
        return '<Robot {}>'.format(self.name)

    @property
    def task_time(self):
        return self.current_time - self.start_time

    def choose_task(self):
        self.current_task = 'mine_foo'

    def update(self):
        self.current_time += 1
        if self.task_time == Robot.TIME_PER_TASK[self.current_task]:
            task = getattr(self, self.current_task)
            task()
            self.reinit_time()
            self.choose_task()

    def reinit_time(self):
        self.start_time = self.current_time

    def mine_foo(self):
        print('calling mine foo for:', self)
        Foobartory.nfoo += 1


if __name__ == '__main__':
    foobartory = Foobartory()
    foobartory.go()
