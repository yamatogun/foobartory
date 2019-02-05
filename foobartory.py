#!/usr/bin/python3

from abc import ABC, abstractmethod
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
    nrobots = 0

    schedule = []  # list of (endtime, agent)

    def __init__(self, nrobots=2):
        super().__init__()

        for _ in range(nrobots):
            robot = Robot()
            self.register_agent(robot)
        self.nrobots += nrobots

        # actions from the foobartory have to be registered as well
        self.register_agent(self)

    @property
    def nfoos(self):
        return len(self.foos)

    @property
    def nbars(self):
        return len(self.bars)

    @property
    def nfoobars(self):
        return len(self.foobars)

    def register_agent(self, agent):
        end_time = agent.get_end_time()
        Foobartory.schedule.append((end_time, agent))
        Foobartory.schedule.sort(key=lambda x: x[0])
        # NB: maybe an orderedict + time segmentation could be a way
        # to deal with high number of robots and prevent
        # from sorting the list all the time
        # Doesn't seem necessary with 100 robots

        self.next_end_time =  Foobartory.schedule[0][0]

    def sell_foobar_and_buy_robots(self):
        # check if there still are foobars first
        if self.foobars:
            nsold_max = min(5, len(self.foobars))
            nsold = random.randint(1, nsold_max)
            for _ in range(nsold):
                self.foobars.pop()
            print('selling {} foobars by Foobartory'.format(nsold))
            Foobartory.money += nsold
        else:
            print('no foobar to sell')

        # handle the case where there are not foos enough anymore
        nrobots = min(self.money // 3, self.nfoos // 6)
        print('{} robots bought'.format(nrobots))
        if nrobots:
            for _ in range(nrobots):
                self.register_agent(Robot())
            self.nrobots += nrobots
            Foobartory.foos = self.foos[:-6*nrobots]
            Foobartory.money -= 3 * nrobots

    def choose_task(self):
        self.current_task = 'sell_foobar_and_buy_robots'

    def get_end_time(self):
        return datetime.datetime.now() + datetime.timedelta(seconds=5)  # 10

    def go(self):
        assert self.schedule, 'there should be at least one robot'
        while True:
            current_time = datetime.datetime.now()
            if current_time >= self.next_end_time:
                agent = Foobartory.schedule.pop(0)[1]

                agent.work()
                print('current_time: ', current_time)
                print('action time: ', self.next_end_time)
                print(
                    'nfoo: ', len(self.foos),
                    '\nnbar: ', len(self.bars),
                    '\nnfoobar: ', len(self.foobars),
                    '\nmoney: ', Foobartory.money,
                    '\nnrobots: ', self.nrobots,
                    '\n'
                )

                if self.nrobots >= 100:
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
        # TODO: replace len by properties
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
