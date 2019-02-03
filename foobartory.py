#!/usr/bin/python3

'''
Single thread implementation
'''

from abc import ABC, abstractmethod
from collections import OrderedDict
import datetime
import random
import re
import sys


class Agent(ABC):
    """
    Entity that is assigned a task to perform at a given moment
    Both Foobartory and Robot are Agents
    """
    def __init__(self):
        self.current_task = None
        self.choose_task()
        self.start_time = datetime.datetime.now()

    @abstractmethod
    def choose_task():
        """
        set self.current_task
        """
        pass


    @abstractmethod
    def get_end_time():
        pass

    def work(self):
        print('self.current_task: ', self.current_task)
        task = getattr(self, self.current_task)()
        self.choose_task()
        self.reinit_time()

    def reinit_time(self):
        self.start_time = datetime.datetime.now()


class Foobartory(Agent):
    foos = []
    bars = []
    foobars = []
    money = 0

    schedule = OrderedDict()  # timestamps with corresponding robots

    def __init__(self, nrobots=2):
        super().__init__()

        for _ in range(nrobots):
            robot = Robot()
            self.register_agent(robot)

        # actions from the foobartory have to be registered as well
        self.register_agent(self)

    def register_agent(self, agent):
        end_time = agent.get_end_time()
        self.schedule.setdefault(end_time, [])
        self.schedule[end_time].append(agent)
        self.schedule = OrderedDict(
            sorted(self.schedule.items(), key=lambda x: x[0])
        )
        print(self.schedule)
        self.next_action_time = next(iter(self.schedule.items()))[0]

    def sell_foobar(self):
        # check if there still are foobars first
        if self.foobars:
            nsold_max = min(5, len(self.foobars))
            nsold = random.randint(1, nsold_max)
            for _ in range(nsold):
                self.foobars.pop()
            print('selling {} foobars by Foobartory'.format(nsold))
            self.money += nsold
        else:
            print('no foobar to sell')

    def choose_task(self):
        self.current_task = 'sell_foobar'
        # TODO: complete with buy

    def get_end_time(self):
        if self.current_task == 'sell_foobar':
            duration = 10
        return datetime.datetime.now() + datetime.timedelta(seconds=duration)

    def go(self):
        assert self.schedule, 'there should be at least one robot'
        while True:
            current_time = datetime.datetime.now()
            if current_time >= self.next_action_time:
                agents = self.schedule.popitem(last=False)[1]
                for agent in agents:  # TODO: remove list ?
                    agent.work()

                    #if self.nfoo >= 100:
                    #    sys.exit()

                    print('nfoo: ', len(self.foos), '\nnbar: ', len(self.bars),
                          '\nnfoobar: ', len(self.foobars), '\nmoney: ',
                          self.money)

                    #if len(self.foobars) == 3:
                    #    sys.exit()

                    if self.money >= 20:
                        sys.exit()

                    self.register_agent(agent)


class Robot(Agent):
    robot_counter = 0

    def __init__(self):
        super().__init__()

        self.name = self.robot_counter
        Robot.robot_counter += 1

    def __str__(self):
        return '<Robot {}>'.format(self.name)

    def get_end_time(self):
        if self.current_task == 'mine_foo':
            duration = 1  # TODO: conf ?
        elif self.current_task == 'mine_bar':
            duration = random.uniform(.5, 2)
        elif self.current_task == 'make_foobar':
            duration = 2
        elif 'change' in self.current_task:
            duration = 3  # 20
        else:
            assert False
        return self.start_time + datetime.timedelta(seconds=duration)

    def choose_task(self):
        self.previous_task = self.current_task
        if len(Foobartory.foos) <= 6:  # always keep at least 6 foos to buy robots
            if (
                self.previous_task == 'mine_foo' or
                self.previous_task == 'change_to_foo'
            ):
                self.current_task = 'mine_foo'
            else:
                self.current_task = 'change_to_foo'
        elif Foobartory.bars:
            if (
                self.previous_task == 'make_foobar' or
                self.previous_task == 'change_to_foobar'
            ):
                self.current_task = 'make_foobar'
            else:
                self.current_task = 'change_to_foobar'
        else:  # nfoo > 6 and nbar == 0
            if (
                self.previous_task == 'mine_bar' or
                self.previous_task == 'change_to_bar'
            ):
                self.current_task = 'mine_bar'
            else:
                self.current_task = 'change_to_bar'

    def mine_foo(self):
        print('mining foo with:', self)
        Foobartory.foos.append(Foo())

    def mine_bar(self):
        print('mining bar with :', self)
        Foobartory.bars.append(Bar())

    def make_foobar(self):
        print('making foobar with :', self)
        # first check stocks because it could have change meanwhile
        if Foobartory.foos and Foobartory.bars:
            success = True if random.random() < 0.6 else False
            if success:
                print('create foobar: SUCCESS')
                Foobartory.foobars.append(
                    FooBar(
                        Foobartory.foos.pop(),
                        Foobartory.bars.pop(),
                    )
                )
            else:
                print('create foobar: FAILURE')
                Foobartory.foos.pop()


    def change_to_foo(self):
        pass

    def change_to_bar(self):
        pass

    def change_to_foobar(self):
        pass


class Base:
    ninstances = 0

    def __init__(self):
        self.__class__.ninstances += 1

class Foo(Base):
    def __init__(self):
        super().__init__()
        self.id = 'F{}'.format(self.ninstances)
        print('{} instance n°{}'.format(self.__class__.__name__, self.id))


class Bar(Base):
    def __init__(self):
        super().__init__()
        self.id = 'B{}'.format(self.ninstances)
        print('{} instance n°{}'.format(self.__class__.__name__, self.id))

class FooBar:
    def __init__(self, foo, bar):
        self.id = '{fid}:{bid}'.format(fid=foo.id, bid=bar.id)
        print('created {} n°{}'.format(self.__class__.__name__, self.id))


if __name__ == '__main__':
    foobartory = Foobartory()
    foobartory.go()
