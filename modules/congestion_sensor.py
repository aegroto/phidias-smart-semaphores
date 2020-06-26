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

class AsynchronousCongestionSensorsUpdater(Sensor):
    def on_start(self, locations, congestion_probabilities, min_interval, max_interval):
        self.locations = locations.value
        self.congestion_probabilities = congestion_probabilities.value

        self.min_interval = min_interval.value
        self.max_interval = max_interval.value

        for location in self.locations:
            self.assert_belief(congestion(location))

        self.running = True

    def on_stop(self):
        self.running = False

    def sense(self):
        while self.running:
            time.sleep(random.uniform(self.min_interval, self.max_interval))

            location_index = random.randint(0, len(self.locations))

            location = self.locations[location_index]
            congestion_probability = self.congestion_probabilities[location_index]

            if random.random() < congestion_probability:
                # Congestion
                self.assert_belief(congestion(location))
            else:
                self.retract_belief(congestion(location))
