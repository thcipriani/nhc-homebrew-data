#!/usr/bin/env python
import os
import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

base = os.path.dirname(__file__)
db_file = os.path.join(base, '..', 'nhc.db')
conn = sqlite3.connect(db_file)

years = YearLocator()   # every year
months = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')

date_range = range(2005, 2015)
gravities = [];
dates = []

for year in date_range:
    dates.append(datetime.date(year, 1, 1))
    query = 'select specs from recipes where specs <> "None" and year="%s"' % year

    cur = conn.execute(query)
    arr = []

    while True:
        row = cur.fetchone()

        if row == None:
            break

        grav = row[0].split('\n')[0].split(' ')[1]
        if '-' in grav:
            grav = grav.split('-')[0]

        arr.append(float(grav))

    avg = reduce(lambda x, y: x + y, arr) / len(arr)
    gravities.append(avg)

conn.close()

fig, ax = plt.subplots()
ax.plot_date(dates, gravities, '-')

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

def gravity(x):
    return '%1.4f' % x

ax.fmt_xdata = DateFormatter('%Y')
ax.fmt_ydata = gravity
ax.grid(True)

fig.autofmt_xdate()
plt.show()
