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
        +INCOMING_CAR(C)[{'from': SENDER}] >> [
            show_line("[", self.name(), "] Incoming car (sender: ", SENDER, ")"),
            +car(C, self.name())
        ]

        # Update loop 
        +UPDATE()[{'from': SENDER}] >> [
            show_line("[", self.name(), "] Running update tick (sender: ", SENDER, ")"),
            move_cars(),
        ]

        move_cars() >> [
            show_line("[", self.name(), "] Moving cars"),
        ]
