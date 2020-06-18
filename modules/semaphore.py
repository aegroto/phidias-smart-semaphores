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
        next_state() / (sem_state("red") & standby(self.name())) >> [
            show_line("[", self.name(), "] Next state is green"),
            sem_state("green")
        ]

        next_state() / (sem_state("green") & standby(self.name())) >> [
            show_line("[", self.name(), "] Next state is yellow"),
            sem_state("yellow")
        ]

        next_state() / (sem_state("yellow") & standby(self.name())) >> [
            show_line("[", self.name(), "] Next state is red"),
            sem_state("red")
        ]

        next_state() >> [
            show_line("[", self.name(), "] Turning on to: green"),
            sem_state("green"),
            +congestion(self.name())
        ]

        +standby(self.name())[{'from': SENDER}] >> [
            show_line("[", self.name(), "] There's no congestion, fixing state to yellow"),
            sem_state("yellow")
        ]

        -standby(self.name())[{'from': SENDER}] >> [
            show_line("[", self.name(), "] Congestion, restoring cycle"),
            # sem_state("yellow")
        ]

        +SWITCH_SEMSTATE(SEMID)[{'from': SENDER}] / (eq(SEMID, self.name()))>> [
            show_line("[", self.name(), "] Updating semaphore state (sender: ", SENDER, ")"),
            next_state()
        ]

        move_cars()['all'] / (sem_state("red")) >> [
            # This should not do anything
        ]

        super().main()
