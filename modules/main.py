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

        # Goals
        on_destination(C) << (car(C, L) & eq(L, 'B'))

        # Simulation procedures
        simulate() >> [
            show_line("Starting simulation..."),
            +active(),
            RoadStateUpdater(["A", "B"], ["Sem1", "Sem2"], 1.0, 10).start,
            # CarSpawner(0.1, 0.1, "A").start

            CongestionSensorsUpdater(["Sem1", "Sem2"], 1.0, 2.0, 0.0).start,
        ]

        stop() >> [
            show_line("Stopping simulation..."),
            -active()
        ]

        # Congestion system 
        +congestion(L) / (active() & sem(SEMID)) >> [
            show_line("[", self.name(), "] Detected congestion at ", L),
            -standby(SEMID)[{'to': SEMID}]
        ]

        -congestion(L) / (active() & sem(L) & congestion(L)) >> [
            show_line("[", self.name(), "] Detected low congestion at ", L)
        ]

        -congestion(L)['all'] / (active() & sem(SEMID)) >> [
            show_line("[", self.name(), "] Detected low congestion at ", L, ". All crossroads are not congested, disabling semaphores."),
            send_congestion_notification(SEMID)
        ]

        send_congestion_notification(SEMID)['all'] / sem(SEMID) >> [
            show_line("[", self.name(), "] Sending standby notification to ", SEMID),
            +standby(SEMID)[{'to': SEMID}]
        ]

        # Update loops
        +SWITCH_SEMSTATE(SEMID) / (active() & eq(SEMID, SEMID)) >> [
            # show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to switch its state"),
            +SWITCH_SEMSTATE(SEMID)[{'to': SEMID}]
        ]

        +UPDATE(SEMID) / (active() & eq(SEMID, SEMID)) >> [
            # show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to update its state"),
            +UPDATE(SEMID)[{'to': SEMID}],
        ]

        # Cars movement
        +SPAWN_CAR(C, L) / active() >> [
            # show_line("[", self.name(), "] Spawning car ", C, " at location ", L),
            # +INCOMING_CAR(C)[{'to': L}],
            +car(C, L)
        ]

        +MOVE_CARS_TO(L)[{'from': SENDER}]  >> [
            # show_line("[", self.name(), "] Movings cars from ", SENDER, " to ", L),
            move_cars(SENDER, L)
        ]

        move_cars(SENDER, L)['all'] / car(C, SENDER) >> [
            -car(C, SENDER),
            +car(C, L)
        ]