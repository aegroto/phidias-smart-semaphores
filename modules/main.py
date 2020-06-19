import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.state_updater import *

from modules.environment import *
from modules.car_spawner import *
from modules.congestion_sensor import *

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        # Debug procedures
        # populate()['all'] >> [
        #     show_line("Populating the road..."),
        #     +INCOMING_CAR(0)[{'to': 'Sem1'}]
        # ]

        cars_at(SEMID)['all'] / car(C, SEMID) >> [
            show_line(C),
        ]

        sems()['all'] / sem(SEMID) >> [
            show_line(SEMID),
        ]

        # Goals
        on_destination(C) << (car(C, L) & eq(L, 'B'))

        # Simulation procedures
        simulate() >> [
            show_line("Starting simulation..."),
            +active(self.name()),
            RoadStateUpdater(["A", "B"], ["Sem1", "Sem2"], 0.3, 10).start,
            CarSpawner(0.1, 0.3, "A").start,

            CongestionSensorsUpdater(["Sem1", "Sem2"], 2.0, 5.0, 0.5).start,
        ]

        stop() >> [
            show_line("Stopping simulation..."),
            -active(self.name())
        ]

        # Congestion system 
        +congestion(L) / (active(self.name()) & sem(SEMID) & neq(SEMID, L) & congestion(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Detected congestion at ", L),
        ]

        +congestion(L) / (active(self.name()) & sem(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Detected congestion at ", L, " semaphores were in standby, restoring cycle"),
            send_congestion_notification()
        ]

        -congestion(L) / (active(self.name()) & sem(L) & sem(SEMID) & congestion(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Detected low traffic at ", L)
        ]

        -congestion(L) / (active(self.name()) & sem(L)) >> [
            show_line("[", self.name(), " - congestion] Detected low traffic at ", L, ". All crossroads result uncongested, disabling semaphores."),
            send_decongestion_notification()
        ]

        send_decongestion_notification()['all'] / (active(self.name()) & sem(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Sending standby notification to ", SEMID),
            +standby(SEMID)[{'to': SEMID}]
        ]

        send_congestion_notification()['all'] / (active(self.name()) & sem(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Sending cycle restore notification to ", SEMID),
            -standby(SEMID)[{'to': SEMID}]
        ]

        # Update loops
        +SWITCH_SEMSTATE(SEMID) / (active(self.name()) & eq(SEMID, SEMID)) >> [
            # show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to switch its state"),
            +SWITCH_SEMSTATE(SEMID)[{'to': SEMID}]
        ]

        +UPDATE(SEMID) / (active(self.name()) & eq(SEMID, SEMID)) >> [
            # show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to update its state"),
            +UPDATE(SEMID)[{'to': SEMID}],
        ]

        # Cars movement
        +SPAWN_CAR(C, L) / active(self.name()) >> [
            show_line("[", self.name(), " - cars] Spawning car ", C, " at location ", L),
            # +INCOMING_CAR(C)[{'to': L}],
            +car(C, L)
        ]

        +MOVE_CARS_TO(L)[{'from': SENDER}] / car(C, SENDER) >> [
            show_line("[", self.name(), " - cars] Movings cars from ", SENDER, " to ", L),
            move_cars(SENDER, L)
        ]

        move_cars(SENDER, L)['all'] / car(C, SENDER) >> [
            -car(C, SENDER),
            +car(C, L)
        ]