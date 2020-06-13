import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

class semaphore(Agent):
    def main(self):
        +UPDATE_SEMSTATE()[{'from': SENDER}] >> [
            show_line("[", self.name(), "] Updating semaphore state (sender: ", SENDER, ")"),
            next_state(self.name())
        ]

        next_state(SEMID) / (red(SEMID)) >> [
            show_line("[", self.name(), "] Next state is green"),
            -red(SEMID),
            +green(SEMID)
        ]

        next_state(SEMID) / (green(SEMID)) >> [
            show_line("[", self.name(), "] Next state is yellow"),
            -green(SEMID),
            +yellow(SEMID)
        ]

        next_state(SEMID) / (yellow(SEMID)) >> [
            show_line("[", self.name(), "] Next state is red"),
            -yellow(SEMID),
            +red(SEMID)
        ]

        next_state(SEMID) >> [
            show_line("[", self.name(), "] Turning on to: red"),
            +red(SEMID)
        ]