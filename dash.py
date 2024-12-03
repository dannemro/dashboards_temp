from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Range1d
from pylsl import StreamInlet, resolve_stream

# EEG parameters
SAMPLE_RATE = 500  # Sampling rate in Hz
WINDOW_SIZE = 11  # Time window to display in seconds
CHANNEL_OFFSET = 100  # Vertical offset between channels

# Resolve LSL stream
print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
print("EEG stream found!")

# Get number of channels from the stream info
EEG_CHANNELS = inlet.info().channel_count()
print(f"Number of EEG channels: {EEG_CHANNELS}")

# Create Bokeh data source
# Dynamically create keys for the data source based on the number of channels
data = {'time': []}
for i in range(EEG_CHANNELS):
    data[f'eeg{i+1}'] = []
source = ColumnDataSource(data=data)

# Create Bokeh plot
p = figure(plot_width=1000, plot_height=600, title="Multichannel EEG Data", x_range=(0, WINDOW_SIZE))
p.xaxis.axis_label = "Time (s)"
p.yaxis.axis_label = "Amplitude (µV)"

# Add glyphs for each EEG channel with offsets
for i in range(EEG_CHANNELS):
    # Add the offset to the y-values in the data source
    p.line(x='time', y=f'eeg{i+1}', source=source, line_width=2, legend_label=f'Channel {i+1}')

# Adjust y-axis range to accommodate offsets
p.y_range = Range1d(start=-CHANNEL_OFFSET, end=EEG_CHANNELS * CHANNEL_OFFSET)

# Update function
def update():
    # Get new EEG data
    sample, timestamp = inlet.pull_sample()

    # Append new data to source with offsets
    new_data = {'time': [source.data['time'][-1] + 1 / SAMPLE_RATE if source.data['time'] else 0]}
    for i in range(EEG_CHANNELS):
        new_data[f'eeg{i+1}'] = [sample[i] + i * CHANNEL_OFFSET]
    source.stream(new_data, rollover=int(SAMPLE_RATE * WINDOW_SIZE))

    # Update x-axis range
    p.x_range.start = source.data['time'][-1] - WINDOW_SIZE
    p.x_range.end = source.data['time'][-1]

# Add periodic callback for updating the plot
curdoc().add_periodic_callback(update, 1000 / SAMPLE_RATE)

# Show the plot
curdoc().add_root(column(p))