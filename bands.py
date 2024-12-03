from bokeh.plotting import curdoc, figure
from bokeh.models import ColumnDataSource, Slider
import time

from matplotlib import pyplot as plt
from mne import set_log_level

from mne_lsl.player import PlayerLSL as Player
from mne_lsl.stream import StreamLSL as Stream
from dash_utils import bandpower
import random
import numpy as np


set_log_level("WARNING")

# retrieve the sample data
stream = Stream(bufsize=2, source_id='acquisition').connect()
stream.pick("eeg") 
stream.set_eeg_reference("average")
mapping = dict(zip(stream.ch_names, ['stim']+['eeg']*68+['eog']*4))
stream.set_channel_types(mapping)

curdoc().theme = "dark_minimal"

names = ['delta', 'theta', 'alpha', 'beta', 'gamma']
lims = [(0.5, 4), (4, 8), (8, 13), (13, 30), (30, 50)]
tools = "lasso_select,box_zoom,tap"

# Initial data
data_init = {'names': names, 'values': [0]*5}

# Create a ColumnDataSource
source = ColumnDataSource(data=data_init)

# Create the plot
p = figure(x_range=names, height=500, width=1000, title="Dynamic Bar Plot",
           toolbar_location=None, tools=tools)

# Add the bars to the plot
p.vbar(x='names', top='values', width=0.9, source=source)

# Format the plot
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.y_range.end = 0.15
p.xaxis.major_label_orientation = "horizontal"



def update_data():
  """Pulls data from the LSL stream, averages it, and updates the plot."""
  # Pull data (e.g., 1 second)
  data, ts = stream.get_data(2, picks='Oz')
  bp = [bandpower(data, stream.info["sfreq"], "periodogram", band=bs) for bs in lims]
  # Average data per channel
  # Update the plot
  source.data = {'names': names, 'values': bp}

curdoc().add_periodic_callback(update_data, 1000)  # Update every 1 second
curdoc().add_root(p)


