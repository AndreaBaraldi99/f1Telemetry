import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import functools

import fastf1

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def rotate_single(x, y, angle):
    rot_x = x * np.cos(angle) - y * np.sin(angle)
    rot_y = x * np.sin(angle) + y * np.cos(angle)
    return rot_x, rot_y

session = fastf1.get_session(2024, 'Monza', 'FP1')
session.load()

lap = session.laps.pick_fastest()
pos = lap.get_pos_data()

lec_lap = session.laps.pick_driver("ANT").get_telemetry()
ver_lap = session.laps.pick_driver("VER").get_telemetry()
ham_lap = session.laps.pick_driver("HAM").get_telemetry()


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
point, = ax.plot(0, 0, "o", markersize=8, color='red')
ham_point, = ax.plot(0, 0, "o", markersize=8, color='grey')
ver_point, = ax.plot(0, 0, "o", markersize=8, color='blue')
text = ax.text(0, 0, "ANT")
ham_text = ax.text(0, 0, "HAM")
ver_text = ax.text(0, 0, "VER")
#speed = fig.text(0.1, 0.9, "SPEED")


def animate(frame_num):
    rot_x = lec_lap['X'].to_list()[frame_num] * np.cos(track_angle) - lec_lap['Y'].to_list()[frame_num] * np.sin(track_angle)
    rot_y = lec_lap['X'].to_list()[frame_num] * np.sin(track_angle) + lec_lap['Y'].to_list()[frame_num] * np.cos(track_angle)
    rot_x_ham, rot_y_ham = rotate_single(ham_lap['X'].to_list()[frame_num], ham_lap['Y'].to_list()[frame_num], track_angle)
    rot_x_ver, rot_y_ver = rotate_single(ver_lap['X'].to_list()[frame_num], ver_lap['Y'].to_list()[frame_num], track_angle)
    point.set_data([rot_x], [rot_y])
    ham_point.set_data([rot_x_ham],[rot_y_ham])
    ver_point.set_data([rot_x_ver],[rot_y_ver])
    text.set_position((rot_x, rot_y))
    ham_text.set_position((rot_x_ham, rot_y_ham))
    ver_text.set_position((rot_x_ver, rot_y_ver))
    return point
    
plt.title(session.event['Location'])
plt.xticks([])
plt.yticks([])
plt.axis('equal')

anim = animation.FuncAnimation(fig, animate, interval=20)

plt.show()