import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

from modules.state_updater import *
from modules.car_spawner import *
from modules.congestion_sensor import *
from modules.roadpoint import *
from modules.semaphore import *
from modules.timer import *

def_vars(
    # Simulation parameters
    "STATE_UPDATE_TIME_INTERVAL",
    "SEM_STATE_CHANGE_TICKS",
    "CAR_SPAWN_INTERVAL",
    "CAR_SPAWN_PROBABILITY",
    "SIMULATION_TIME",

    # Congestion sensors parameters
    "MIN_SENSORS_DETECT_TIME_INTERVAL",
    "MAX_SENSORS_DETECT_TIME_INTERVAL",
    "CONGESTION_LEVEL",
)

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        cars_at(SEMID)['all'] / car(C, SEMID) >> [
            show_line(C),
        ]

        sems()['all'] / sem(SEMID) >> [
            show_line(SEMID),
        ]

        # Goals
        on_destination(C) << (car(C, L) & eq(L, 'B'))

        # Simulation 
        simulate_without_sensors(STATE_UPDATE_TIME_INTERVAL, SEM_STATE_CHANGE_TICKS, CAR_SPAWN_INTERVAL, CAR_SPAWN_PROBABILITY, SIMULATION_TIME) >> [
            show_line("Starting simulation..."),
            +active(self.name()),
            RoadStateUpdater(["A", "B"], ["Sem1", "Sem2"], STATE_UPDATE_TIME_INTERVAL, SEM_STATE_CHANGE_TICKS).start,
            CarSpawner(CAR_SPAWN_INTERVAL, CAR_SPAWN_PROBABILITY, "A").start,

            SimulationTimer(SIMULATION_TIME).start
        ]
        
        simulate_with_sensors(STATE_UPDATE_TIME_INTERVAL, SEM_STATE_CHANGE_TICKS, CAR_SPAWN_INTERVAL, CAR_SPAWN_PROBABILITY, SIMULATION_TIME, MIN_SENSORS_DETECT_TIME_INTERVAL, MAX_SENSORS_DETECT_TIME_INTERVAL, CONGESTION_LEVEL) >> [
            show_line("Starting simulation... (", CONGESTION_LEVEL, ")"),
            +active(self.name()),
            RoadStateUpdater(["A", "B"], ["Sem1", "Sem2"], STATE_UPDATE_TIME_INTERVAL, SEM_STATE_CHANGE_TICKS).start,
            CarSpawner(CAR_SPAWN_INTERVAL, CAR_SPAWN_PROBABILITY, "A").start,

            ThresholdedAsynchronousCongestionSensorsUpdater(["Sem1", "Sem2"], CONGESTION_LEVEL, MIN_SENSORS_DETECT_TIME_INTERVAL, MAX_SENSORS_DETECT_TIME_INTERVAL).start,
            SimulationTimer(SIMULATION_TIME).start
        ]

        +TIMEOUT("ON") >> [
            show_line("Timeout"),
            stop()
        ]

        stop() >> [
            show_line("Stopping simulation..."),
            -active(self.name()),
            show_line("# --- RESULTS --- #"),
            extract_cars_from("B")
        ]

        extract_cars_from(LOC) >> [
            extract_cars_from(LOC, 0)
        ]

        extract_cars_from(LOC, N) / (car(C, L) & eq(L, LOC)) >> [
            "N = N + 1",
            -car(C, L),
            extract_cars_from(LOC, N)
        ]

        extract_cars_from(LOC, N) >> [
            show_line("Cars extracted from ", LOC , ": ", N)
        ]

        # Congestion system 
        +congestion(L) / (active(self.name()) & sem(SEMID) & neq(SEMID, L) & congestion(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Detected congestion at ", L),
        ]

        +congestion(L) / (active(self.name()) & sem(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Detected congestion at ", L, ", semaphores were in standby, restoring cycle"),
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
            +LOW_TRAFFIC(SEMID)[{'to': SEMID}]
        ]

        send_congestion_notification()['all'] / (active(self.name()) & sem(SEMID)) >> [
            show_line("[", self.name(), " - congestion] Sending cycle restore notification to ", SEMID),
            +CONGESTION(SEMID)[{'to': SEMID}]
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
            show_line("[", self.name(), " - cars] Moving cars from ", SENDER, " to ", L),
            move_cars(SENDER, L)
        ]

        move_cars(SENDER, L) / car(C, SENDER) >> [
            show_line("[", self.name(), " - cars] Moving car ", C ," from ", SENDER, " to ", L),
            -car(C, SENDER),
            +car(C, L)
        ]

# start the actors
RoadPoint("A", "Sem1").start()
Semaphore("Sem1", "Sem2").start()
Semaphore("Sem2", "B").start()
GoalRoadPoint("B").start()

PHIDIAS.assert_belief(roadpoint("A"))
PHIDIAS.assert_belief(roadpoint("Sem1"))
PHIDIAS.assert_belief(roadpoint("Sem2"))
PHIDIAS.assert_belief(roadpoint("B"))

PHIDIAS.assert_belief(sem("Sem1"))
PHIDIAS.assert_belief(sem("Sem2"))

main().start()

# PHIDIAS.assert_belief(active("main"))
# PHIDIAS.assert_belief(congestion("Sem1"))
# PHIDIAS.assert_belief(congestion("Sem2"))

# run the engine shell
PHIDIAS.shell(globals())

# simulate_with_sensors(0.2, 50, 0.1, 0.2, 60, 2.0, 5.0, 0.8, 0.9)