import pandas as pd
import matplotlib.pyplot as plt
#import random
from matplotlib.animation import FuncAnimation
from itertools import count
plt.style.use('fivethirtyeight')

#x_vals = [4, 3]
#y_vals = [2, 5]
#index = count()

#plt.plot(x_vals, y_vals)


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y = data['y_value']
    z = data['z_value']  # Assuming 'z_value' is the column name for your z-axis data
    ax.clear()
    ax.scatter(x, y, z, c='r', marker='o', label='Position')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_xlim([100, 500])
    ax.set_ylim([-100, 100])
    ax.set_zlim([-50, 300])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

plt.tight_layout()
plt.show()