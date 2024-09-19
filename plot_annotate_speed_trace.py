"""Plot speed traces with corner annotations
============================================

Plot the speed over the course of a lap and add annotations to mark corners.
"""


import matplotlib.pyplot as plt

import fastf1.plotting
from timple.timedelta import strftimedelta

def closest(lst, K):

    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]


# Enable Matplotlib patches for plotting timedelta values and load
# FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')

# load a session and its telemetry data
session = fastf1.get_session(2024, 'Italian Grand Prix', 'R')
session.load()

##############################################################################
# First, we select the fastest lap and get the car telemetry data for this
# lap.

fastest_lap = session.laps.pick_drivers("HAM").pick_fastest()
car_data = fastest_lap.get_car_data().add_distance()

fastest_lap_lec = session.laps.pick_drivers("LEC").pick_fastest()
car_data_lec = fastest_lap_lec.get_car_data().add_distance()

fastest_lap_nor = session.laps.pick_drivers("NOR").pick_fastest()
car_data_nor = fastest_lap_nor.get_car_data().add_distance()

max_speed_corner = []
filter = True
for i in range(0, len(fastest_lap_lec.telemetry['Brake'].to_list())):
    if(fastest_lap_lec.telemetry['Brake'].to_list()[i] == True and filter):
        dist = closest(fastest_lap.telemetry['Distance'].to_list(), fastest_lap_lec.telemetry['Distance'].to_list()[i])
        sp = fastest_lap.telemetry.loc[fastest_lap.telemetry['Distance'] == dist, 'Speed'].iloc[0]

        max_speed_corner.append((fastest_lap_lec.telemetry['Distance'].to_list()[i], fastest_lap_lec.telemetry['Speed'].to_list()[i], sp))
        filter = False
    if(fastest_lap_lec.telemetry['Brake'].to_list()[i] == False):
        filter = True    

del max_speed_corner[1]
#print(max_speed_corner)

##############################################################################
# Next, load the circuit info that includes the information about the location
# of the corners.

circuit_info = session.get_circuit_info()

##############################################################################
# Finally, we create a plot and plot the speed trace as well as the corner
# markers.

team_color = fastf1.plotting.get_team_color(fastest_lap['Team'],
                                            session=session)
team_color_lec = fastf1.plotting.get_team_color(fastest_lap_lec['Team'],
                                            session=session)
team_color_nor = fastf1.plotting.get_team_color(fastest_lap_nor['Team'],
                                            session=session)

fig, ax = plt.subplots()
ax.plot(car_data['Distance'], car_data['Speed'], color=team_color, label=f"{strftimedelta(fastest_lap['LapTime'], '%m:%s.%ms')} {fastest_lap['Driver']}")
ax.plot(car_data_lec['Distance'], car_data_lec['Speed'],
        color=team_color_lec, label=f"{strftimedelta(fastest_lap_lec['LapTime'], '%m:%s.%ms')} {fastest_lap_lec['Driver']}")
ax.plot(car_data_nor['Distance'], car_data_nor['Speed'],
        color=team_color_nor, label=f"{strftimedelta(fastest_lap_nor['LapTime'], '%m:%s.%ms')} {fastest_lap_nor['Driver']}")

# Draw vertical dotted lines at each corner that range from slightly below the
# minimum speed to slightly above the maximum speed.
v_min = car_data['Speed'].min()
v_max = car_data['Speed'].max()
ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min-20, ymax=v_max,
          linestyles='dotted', colors='grey')

# Plot the corner number just below each vertical line.
# For corners that are very close together, the text may overlap. A more
# complicated approach would be necessary to reliably prevent this.
for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax.text(corner['Distance'], v_min-30, txt,
            va='center_baseline', ha='center', size='small')

corner_start = []

#for c in max_speed_corner:
    #text = f'+ {abs(c[1] - c[2])}'
    #if c[1] > c[2]:
        #text += ' LEC'
    #else:
        #text += ' HAM'
    #ax.text(c[0], v_max + 10, text,
            #va='center_baseline', ha='center', size='small')
    #corner_start.append(c[0])
    
    
#ax.vlines(x=corner_start, ymin=v_min-20, ymax=v_max+5,
          #linestyles='dotted', colors='white')


ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')
ax.legend()

# Manually adjust the y-axis limits to include the corner numbers, because
# Matplotlib does not automatically account for text that was manually added.
ax.set_ylim([v_min - 40, v_max + 20])

plt.show()
