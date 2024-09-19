import fastf1 as ff1

session = ff1.get_session(1988, 'Monza', 'Q')
session.load()
print(session.drivers)