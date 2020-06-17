import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *
from modules.roadpoint import RoadPoint

class Semaphore(RoadPoint):
    def main(self):
        # Change state
        next_state(SEMID) / (sem_state("red")) >> [
            show_line("[", self.name(), "] Next state is green"),
            sem_state("green")
        ]

        next_state() / (sem_state("green")) >> [
            show_line("[", self.name(), "] Next state is yellow"),
            sem_state("yellow")
        ]

        next_state() / (sem_state("yellow")) >> [
            show_line("[", self.name(), "] Next state is red"),
            sem_state("red")
        ]

        next_state() >> [
            show_line("[", self.name(), "] Turning on to: green"),
            sem_state("green")
        ]

        +SWITCH_SEMSTATE(SEMID)[{'from': SENDER}] / (eq(SEMID, self.name()))>> [
            show_line("[", self.name(), "] Updating semaphore state (sender: ", SENDER, ")"),
            next_state()
        ]

        move_cars()['all'] / (sem_state("red")) >> [
            # This should not do anything
        ]

        super().main()
