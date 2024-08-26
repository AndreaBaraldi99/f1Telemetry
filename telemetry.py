from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from fastf1.ergast import Ergast
from pathlib import Path

def get_data(year_name, circuit_name, session_name, driver_name):
    session = fastf1.get_session(int(year_name), circuit_name, session_name)
    session.load()
    driver = session.laps.pick_driver(driver_name)
    car_data = driver.get_car_data()
    pos_data = driver.get_pos_data()
    Path(f"./Telemetry/{year_name}/{circuit_name}/{session_name}").mkdir(parents=True, exist_ok=True)
    driver_info = session.get_driver(driver_name)
    ergast = Ergast()
    circuit = ergast.get_circuits(season=year_name, round=session.event.RoundNumber)['circuitName'].iloc[0]
    PATH = f'./Telemetry/{year_name}/{circuit_name}/{session_name}/{driver_name}_{session_name}_{year_name}_{circuit_name}_car_data.csv'
    with open(PATH,'w+') as fd:
        fd.write('F1 for AiM\n')
        fd.write(f"Racer,{driver_info['FullName']}\n")
        fd.write(f"Vehicle,{driver_info['TeamName']}\n")
        fd.write(f"Track,{circuit}\n")
        fd.write(f"Championship,Season {year_name}\n")
        fd.write("Car_data\n")
    car_data.to_csv(PATH, index=False, float_format='%.10f', mode='a')
    with open(PATH,'a') as fd:
        fd.write("Pos_data\n")
    pos_data.to_csv(PATH, index=False, float_format='%.10f', mode='a')
    with open(PATH,'a') as fd:
        fd.write("Lap_data\n")
    driver.to_csv(PATH, index=False, float_format='%.10f', mode='a')

def get_season(year_name):
    ergast = Ergast()
    season = ergast.get_race_schedule(year_name)
    return season['raceName'].tolist()

def get_drivers(year_name, circuit_name, session_name):
    session = fastf1.get_session(int(year_name), circuit_name, session_name)
    session.load()
    drivers_num = session.drivers
    drivers_name = []
    for driver in drivers_num:
        if not session.laps.pick_drivers(driver).empty:
            drivers_name.append(session.laps.pick_drivers(driver)['Driver'].iloc[0])
    return drivers_name, drivers_num


ergast = Ergast()
season = ergast.get_race_schedule(2024)
enter = False
for race in season['raceName']:
    if race == 'Italian Grand Prix':
        break
    if race == 'Hungarian Grand Prix':
        enter = True
    if enter:
        for i in range(1, 6):
            event_name = fastf1.get_event(2024, race).get_session_name(i)
            driver_name, driver_num = get_drivers(2024, race, event_name)
            for driver in driver_name:
                get_data('2024', race, event_name, driver)

""" ergast = Ergast()
driver_name, driver_num = get_drivers(2024, 'Dutch Grand Prix', 'R')
for driver in driver_name:
    get_data('2024', 'Dutch Grand Prix', 'R', driver) """