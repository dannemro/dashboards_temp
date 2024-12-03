from bokeh.plotting import figure, curdoc
from bokeh.layouts import row, column
from bokeh.models import CheckboxGroup, ColumnDataSource

# Sample data and figures (you can add more)
sources = {
    "fig1": ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[6, 7, 2, 4, 5])),
    "fig2": ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[2, 5, 8, 2, 7])),
    "fig3": ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[1, 4, 2, 6, 3]))
}

figures = {
    "fig1": figure(title="Figure 1"),
    "fig2": figure(title="Figure 2"),
    "fig3": figure(title="Figure 3")
}

# Add glyphs to figures
figures["fig1"].circle(x='x', y='y', source=sources["fig1"], size=10)
figures["fig2"].line(x='x', y='y', source=sources["fig2"], line_width=2)
figures["fig3"].vbar(x='x', top='y', source=sources["fig3"], width=0.5)

# Initially hide all figures
for fig in figures.values():
    fig.visible = False

# Create a CheckboxGroup widget
checkbox_group = CheckboxGroup(
    labels=list(figures.keys()), active=[]  # Initially, no figures are selected
)

# Define the callback function
def checkbox_handler(attr, old, new):
    active_figures = [checkbox_group.labels[i] for i in checkbox_group.active]
    for key, fig in figures.items():
        fig.visible = key in active_figures

# Attach the callback to the checkbox group
checkbox_group.on_change('active', checkbox_handler)

# Create the layout
layout = column(checkbox_group, *figures.values())  # Arrange widgets and figures

# Add the layout to the current document
curdoc().add_root(layout)