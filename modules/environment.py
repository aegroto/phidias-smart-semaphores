import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class Car(Belief): pass

class red(Belief): pass
class yellow(Belief): pass
class green(Belief): pass

class active(SingletonBelief): pass

class UPDATE_SEMSTATE(Reactor): pass

class next_state(Procedure): pass

class stop(Procedure): pass
class simulate(Procedure): pass

def_vars("SENDER", "SEMID", "CURRENT_STATE", "Sem1", "Sem2")