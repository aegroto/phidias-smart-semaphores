import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

class CarSpawner(Sensor):
    def on_start(self, tick_time, probability, spawn_location):
        self.tick_time = tick_time.value
        self.probability = probability.value
        self.spawn_location = spawn_location.value

        self.next_car_id = 0

        self.running = True

    def on_stop(self):
        self.running = False

    def sense(self):
        while self.running:
            time.sleep(self.tick_time)

            if random.random() < self.probability:
                self.__spawn_car()

    def __spawn_car(self):
            PHIDIAS.assert_belief(SPAWN_CAR(self.next_car_id, self.spawn_location))

            self.next_car_id += 1
