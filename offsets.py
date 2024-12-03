from bokeh.plotting import curdoc, figure
from bokeh.models import ColumnDataSource, Slider
import time

from matplotlib import pyplot as plt
from mne import set_log_level

from mne_lsl.datasets import sample
from mne_lsl.player import PlayerLSL as Player
from mne_lsl.stream import StreamLSL as Stream
import random
import numpy as np


set_log_level("WARNING")

# retrieve the sample data
stream = Stream(bufsize=2, source_id='eeg_simulation').connect()
stream.pick("eeg") 
stream.set_eeg_reference("average")
data, ts = stream.get_data(2, picks='eeg')
names = stream.info['ch_names'] [1:]
n_channels = len(names)

# Initial data
data_init = {'names': names, 'values': np.mean(data[1:,:], axis=1)}

# Create a ColumnDataSource
source = ColumnDataSource(data=data_init)

# Create the plot
p = figure(x_range=names, height=500, width=1000, title="Dynamic Bar Plot",
           toolbar_location=None, tools="")

# Add the bars to the plot
p.vbar(x='names', top='values', width=0.9, source=source)

# Format the plot
p.xgrid.grid_line_color = None
p.y_range.start = -0.1
p.xaxis.major_label_orientation = "vertical"



def update_data():
  """Pulls data from the LSL stream, averages it, and updates the plot."""
  # Pull data (e.g., 1 second)
  data, ts = stream.get_data(2, picks='eeg')

  # Average data per channel
  avg_data = np.mean(data[1:,:], axis=1)
  # avg_data = [random.randint(0, 1)*-10000 for _ in range(len(names))]
  # print(len(avg_data))
  # Update the plot
  source.data = {'names': names, 'values': avg_data}

curdoc().add_periodic_callback(update_data, 1000)  # Update every 1 second
curdoc().add_root(p)


