__author__ = 'robertevans'

import json
import matplotlib.pyplot as plt


def plot_file(json_file):
    try:
        with open(json_file, 'r') as events_file:
            data = json.load(events_file)
            events = {int(index): int(type_) for index, type_ in data['event_annotations'].items()}
            indexes, types = zip(*events.items())
            plt.stem(indexes, types)
            plt.show()
    except Exception, e:
        print e