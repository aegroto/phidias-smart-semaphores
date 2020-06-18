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

class SWITCH_SEMSTATE(Reactor): pass
class INCOMING_CAR(Reactor): pass
class SPAWN_CAR(Reactor): pass
class UPDATE(Reactor): pass
class MOVE_CARS_TO(Reactor): pass

class next_state(Procedure): pass
class move_car(Procedure): pass
class move_cars(Procedure): pass
class send_congestion_notification(Procedure): pass
class send_decongestion_notification(Procedure): pass

class stop(Procedure): pass
class simulate(Procedure): pass

# Debug
class populate(Procedure): pass
class cars_at(Procedure): pass
class sems(Procedure): pass

def_vars("SENDER", "SEMID", "C", "L")