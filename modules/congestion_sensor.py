import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

class CongestionSensorsUpdater(Sensor):
    def on_start(self, locations, min_interval, max_interval, congestion_probability):
        self.locations = locations.value

        self.min_interval = min_interval.value
        self.max_interval = max_interval.value

        self.congestion_probability = congestion_probability.value

        for location in self.locations:
            self.assert_belief(congestion(location))

        self.running = True

    def on_stop(self):
        self.running = False

    def sense(self):
        while self.running:
            time.sleep(random.uniform(self.min_interval, self.max_interval))

            location = random.choice(self.locations)

            if random.random() < self.congestion_probability:
                # Congestion
                self.assert_belief(congestion(location))
            else:
                self.retract_belief(congestion(location))
