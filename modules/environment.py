import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class car(Belief): pass
class sem(Belief):pass
class roadpoint(Belief):pass

class congestion(Belief): pass
class standby(Belief): pass

class on_destination(Goal): pass

class sem_state(SingletonBelief): pass

class active(SingletonBelief): pass
class TIMEOUT(SingletonBelief): pass

class SWITCH_SEMSTATE(Reactor): pass
class INCOMING_CAR(Reactor): pass
class SPAWN_CAR(Reactor): pass
class UPDATE(Reactor): pass
class MOVE_CARS_TO(Reactor): pass

class CONGESTION(Reactor): pass
class LOW_TRAFFIC(Reactor): pass

class next_state(Procedure): pass
class move_car(Procedure): pass
class move_cars(Procedure): pass
class send_congestion_notification(Procedure): pass
class send_decongestion_notification(Procedure): pass

class stop(Procedure): pass
class simulate(Procedure): pass
class simulate_without_sensors(Procedure): pass
class simulate_with_sensors(Procedure): pass

class extract_cars_from(Procedure): pass

# Debug
class populate(Procedure): pass
class cars_at(Procedure): pass
class sems(Procedure): pass

def_vars(
    "SENDER", "SEMID", "C", "L", "LOC", "N",

    # Simulation parameters
    "STATE_UPDATE_TIME_INTERVAL",
    "SEM_STATE_CHANGE_TICKS",
    "CAR_SPAWN_INTERVAL",
    "CAR_SPAWN_PROBABILITY",
    "SIMULATION_TIME",

    # Congestion sensors parameters (not necessary if simulating without any traffic detection)
    "MIN_SENSORS_DETECT_TIME_INTERVAL",
    "MAX_SENSORS_DETECT_TIME_INTERVAL",
    "CONGESTION_LEVEL",
)