import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *
from modules.main import main
from modules.semaphore import semaphore

# start the actors
semaphore("Sem1").start()
semaphore("Sem2").start()
main().start()

# run the engine shell
PHIDIAS.shell(globals())