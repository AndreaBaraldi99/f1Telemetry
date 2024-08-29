import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import functools

import fastf1

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

session = fastf1.get_session(2024, 'Silverstone', 'R')
session.load()

lap = session.laps.pick_fastest()
pos = lap.get_pos_data()

lec_lap = session.laps.pick_driver("LEC").get_pos_data()

circuit_info = session.get_circuit_info()

# Get an array of shape [n, 2] where n is the number of points and the second
# axis is x and y.
track = pos.loc[:, ('X', 'Y')].to_numpy()

# Convert the rotation angle from degrees to radian.
track_angle = circuit_info.rotation / 180 * np.pi

# Rotate and plot the track map.
rotated_track = rotate(track, angle=track_angle)
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.plot(rotated_track[:, 0], rotated_track[:, 1])
point, = ax.plot(0, 0, "o", markersize=8)

def animate(frame_num):
    rot_x = lec_lap['X'].to_list()[frame_num] * np.cos(track_angle) - lec_lap['Y'].to_list()[frame_num] * np.sin(track_angle)
    rot_y = lec_lap['X'].to_list()[frame_num] * np.sin(track_angle) + lec_lap['Y'].to_list()[frame_num] * np.cos(track_angle)
    point.set_data([rot_x], [rot_y])
    return point
    
plt.title(session.event['Location'])
plt.xticks([])
plt.yticks([])
plt.axis('equal')

anim = animation.FuncAnimation(fig, animate, interval=20)

plt.show()