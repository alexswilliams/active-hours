#!/usr/bin/env python3

import datetime
import itertools

lines = []

with open('active-hours.csv', 'r') as file:
	for line in file:
		parts = line.strip().split(',')
		dt = datetime.datetime.fromisoformat(parts[0])
		lines.append((dt, parts[1]))

sorted(lines, key=lambda x: x[0].timestamp())
by_days = itertools.groupby(lines, lambda dt: dt[0].date())

for grouping in by_days:
	day = grouping[0]
	data_points = list(grouping[1])

	currently_working = False
	period_start = None
	work_periods = []
	cumulative_minutes = 0

	for hour in range(0, 24):
		for minute in range (0, 60, 5):
			time_under_test = datetime.time(hour=hour, minute=minute)

			data_point = next((x for x in data_points if x[0].time() == time_under_test), None)

			if (data_point != None and data_point[1] == '4'):
				cumulative_minutes = cumulative_minutes + 5
				if not currently_working:
					currently_working = True
					period_start = time_under_test
			else:
				if currently_working:
					currently_working = False
					work_periods.append((period_start, time_under_test))
	
	print('{}, {:.3}, {}'.format(
		day,
		cumulative_minutes / 60.0,
		','.join(['{},{}'.format(x[0].isoformat('minutes'), x[1].isoformat('minutes')) for x in work_periods])))
