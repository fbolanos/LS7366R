#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from copy import deepcopy

## Small class that generates random noise from a gaussian process
class DataGenerator():
    def __init__(self):
        self.y = 0

    def read(self):
        self.y += np.random.normal(0, 1, 1)

        # we must copy the value because otherwise it is being
        # returned as a reference to the variable
        return deepcopy(self.y)


### Real time plot functions ####
## Initialize the plot
def init():
    ax1.set_title("Encoder data plot vs time")
    ax1.set_ylabel("Encoder Value (AU")
    ax1.set_xlabel("Time(reads)")


    return plot_data

# Animate the plot, read the encoder data and plot the data.
def animate(i):
    data = encoder.read()
    
    x_data.append(i)
    y_data.append(data)

    if i >= XLIM_MAX/2:
        ax1.set_xlim([i-XLIM_MAX/2, i+XLIM_MAX/2])
        
    plot_data.set_data(x_data, y_data)




if __name__ == "__main__":
    # this can be replaced by the encoder class
    encoder = DataGenerator()
    INTERVAL = 10 # how fast should we update the plot
    XLIM_MAX = 200 # maximum xlim_value

    # Create the matplotlib figure
    fig = plt.figure(figsize=(10, 4))
    ax1 = fig.add_subplot(111, xlim=(0, XLIM_MAX), ylim=(-50, 50))
    # empty data initially
    plot_data, = ax1.plot([], [])

    x_data  = []
    y_data = []
    
    ani = animation.FuncAnimation(fig, animate, interval=INTERVAL, init_func=init) 
    plt.show()