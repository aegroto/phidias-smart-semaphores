import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

class RoadPoint(Agent):
    def __init__(self, name, next_location):
        super().__init__(name)

        self.next_location = next_location

    def main(self):
        # cars_at()['all'] / car(C) >> [
        #     show_line(C),
        # ]

        # +INCOMING_CAR(C)[{'from': SENDER}] >> [
        #     show_line("[", self.name(), "] Incoming car ", C, " (sender: ", SENDER, ")"),
        #     +car(C)
        # ]

        # Update loop 
        +UPDATE(SEMID)[{'from': SENDER}] / eq(SEMID, self.name())>> [
            # show_line("[", self.name(), "] Running update tick (sender: ", SENDER, ")"),
            move_cars(),
        ]

        move_cars()['all'] >> [ # / car(C) >> [
            show_line("[", self.name(), "] Moving cars"),
            +MOVE_CARS_TO(self.next_location)[{'to': 'main'}]
            # -car(C, self.name())[{'to': 'main'}],
            # +car(C, self.next_location)[{'to': 'main'}]
        ]

        # move_car(C) >> [
        #     show_line("[", self.name(), "] Moving car ", C, " to ", self.next_location),
        #     -car(C),
        #     +INCOMING_CAR(C)[{'to': self.next_location}],
        #     # +car(C)[{'to': self.next_location}],
        # ]

class GoalRoadPoint(RoadPoint):
    def __init__(self, name):
        super().__init__(name, None)

    def main(self):
        move_cars() >> [
            # This should not do anything.
        ]

        super().main()
