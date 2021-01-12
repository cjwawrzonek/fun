import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, time, timedelta

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

NOON_MINUTES = 720
FULL_DAY_MINUTES = 2 * NOON_MINUTES

def parse_date(date_str):
	date = [int(s) for s in date_str.split('-')]
	return date

def parse_time(time_str):
	time_str = time_str.strip()
	if time_str.endswith("AM") or time_str.endswith("PM"):
		time, half = time_str.split(' ')
		hours, mins = time.split(':')
		hours = int(hours)
		mins = int(mins)
		if half == "AM":
			# In the case of 12 AM, this is really based 0 minutes, not 12 * 60 minutes
			hours = hours if hours != 12 else 0
			absolute_mins = 60 * hours + mins
		elif half == "PM":
			absolute_mins = 60 * hours + mins + 720
		else:
			raise ValueError("Unknown time format: {}".format(time_str))
	else:
		# No AM / PM, dealing with military time
		hours, mins = time_str.split(':')
		absolute_mins = 60 * int(hours) + int(mins)

	return absolute_mins


def format_data(days):
	awake_morn = []
	sleep_morn = []
	awake_day = []
	sleep_eve = []
	day_strs = []
	next_day_offset = 0

	for day in days:
		day_strs.append(day['date_str'])

		assert day['wake'] >= 0 and day['wake'] < NOON_MINUTES

		awake_morn.append(next_day_offset)
		sleep_morn.append(day['wake'] - next_day_offset)

		# Arbitrary cut off, but I assume that if I haven't gone to sleep 
		# yet by noon the next day, it flips to noon the previous day.

		# Went to sleep after midnight
		if day['sleep'] < NOON_MINUTES:
			awake_day.append(FULL_DAY_MINUTES - day['wake'])
			sleep_eve.append(0)
			next_day_offset = day['sleep']
		else:
			sleep_min = FULL_DAY_MINUTES - day['sleep']
			if sleep_min < 0:
				print 'day wake str:', day['wake_str']
				print 'day sleep str:', day['sleep_str']
				print 'day sleep:', day['sleep']
				raise ValueError('negative sleep_eve')
			sleep_eve.append(sleep_min)
			awake_day.append(FULL_DAY_MINUTES - (sleep_min + day['wake']))
			next_day_offset = 0

		if awake_morn[-1] + sleep_morn[-1] + awake_day[-1] + sleep_eve[-1] != FULL_DAY_MINUTES:
			print 'day wake:', day['wake_str']
			print 'day sleep:', day['sleep_str']
			raise ValueError('Day does not add to 1420 minutes')

	# for data in awake_morn, sleep_morn, awake_day, sleep_eve:
	# 	for i in range(len(data)):
	# 		data[i] = timedelta(minutes=data[i]) + pd.to_datetime('1970/01/01')
	# 		print data[i]
	return [awake_morn, sleep_morn, awake_day, sleep_eve, day_strs]

def to_data_frame(data):
	dates = []
	segments = []
	types = []
	minutes = []

	# assert all segments have same number of days
	for data_type in data:
		assert len(data_type) == len(data[0])

	for i in range(len(data[0])):
		dates.append(data[-1][i])
		segments.append('awake_morn')
		types.append('awake')
		minutes.append(data[0][i])

		dates.append(data[-1][i])
		segments.append('sleep_morn')
		types.append('sleep')
		minutes.append(data[1][i])

		dates.append(data[-1][i])
		segments.append('awake_day')
		types.append('awake')
		minutes.append(data[2][i])

		dates.append(data[-1][i])
		segments.append('sleep_eve')
		types.append('sleep')
		minutes.append(data[3][i])

	df_dict = {
		'dates': dates, 'segments': segments, 'minutes': minutes, 'types': types
	}
	return pd.DataFrame(data=df_dict)

def plotly_bar(df):
	fig = go.Figure()
	# fig.add_trace(go.Bar(x=df.dates, y=df.minutes))
	fig = px.bar(df, x="dates", y="minutes", color="segments", labels="segments",
		category_orders={'segments': ['awake_morn', 'sleep_morn', 'awake_day', 'sleep_eve']},
		color_discrete_map={'awake_morn': '#00cc65', 'sleep_morn': '#c12524', 'awake_day': '#00cc66', 'sleep_eve': '#c12525'},
		title="2020 Sleep Schedule")
	fig.update_yaxes(range=[0, FULL_DAY_MINUTES])

	fig.update_layout(
	    yaxis = dict(
	        tickmode = 'array',
	        tickvals = [0, 180, 360, 540, 720, 900, 1080, 1260, FULL_DAY_MINUTES],
	        ticktext = ['12:00 AM', '3:00 AM', '6:00 AM', '9:00 AM', '12:00 PM', '3:00 PM', '6:00 PM', '9:00 PM', '12:00 AM']
	    ),
	    xaxis_title="Date",
    	yaxis_title="Time of Day",
	)

	fig.add_trace(go.Scatter(x=['2020-12-28', '2020-12-31'],
		y=[FULL_DAY_MINUTES, FULL_DAY_MINUTES], opacity=0.01, mode='lines',
		line_color='#0099ff', fill='tozeroy', showlegend=False)) # fill down to xaxis
	fig.add_trace(go.Scatter(x=['2020-11-21', '2020-11-29'],
		y=[FULL_DAY_MINUTES, FULL_DAY_MINUTES], opacity=0.01, mode='lines',
		line_color='#0099ff', fill='tozeroy', showlegend=False)) # fill down to xaxis
	fig.add_trace(go.Scatter(x=['2020-10-04', '2020-10-11'],
		y=[FULL_DAY_MINUTES, FULL_DAY_MINUTES], opacity=0.01, mode='lines',
		line_color='#0099ff', fill='tozeroy', name="Vacation")) # fill down to xaxis

	fig.add_trace(go.Scatter(
	    x=['2020-03-13', '2020-03-13'],
	    y=[0, FULL_DAY_MINUTES],
	    mode="lines",
	    line=dict(
	        color="black",
	        width=0.9,
	        dash="dot",
	    ),
	    name='Job Goes Remote'
	))

	fig.add_trace(go.Scatter(
	    x=['2020-07-28', '2020-07-28'],
	    y=[0, FULL_DAY_MINUTES],
	    mode="lines",
	    line=dict(
	        color="black",
	        width=0.9,
	        dash="dashdot",
	    ),
	    name='Girlfriend Moves In'
	))

	fig.add_trace(go.Scatter(
	    x=['2020-9-18', '2020-09-18'],
	    y=[0, FULL_DAY_MINUTES],
	    mode="lines",
	    line=dict(
	        color="black",
	        width=0.9,
	        dash="dash",
	    ),
	    name='Started Coaching'
	))

	# These are some hacks to "merge" the sleep and awake bars in the figure visually
	for trace in fig['data']:
		if trace['name'] == 'sleep_eve':
			trace['showlegend'] = False
		elif trace['name'] == 'sleep_morn':
			trace['name'] = 'Sleep'
		elif trace['name'] == 'awake_morn':
			trace['name'] = 'Awake'
		elif trace['name'] == 'awake_day':
			trace['showlegend'] = False
	fig.show()

def plt_bar(data):
	awake_morn, sleep_morn, awake_day, sleep_eve = data

	assert (len(awake_morn) == len(sleep_morn) == len(awake_day) == len(sleep_eve))

	barWidth = 1

	quarter = ["Q1", "Q2", "Q3", "Q4"]
	# r = range(len(quarter))

	colors = ['#FF9999', '#00BFFF','#C1FFC1','#CAE1FF','#FFDEAD']
	# The position of the bars on the x-axis
	r = range(len(awake_morn))
	plt.figure(figsize=(10,7))

	# Decreasing time on y axis
	plt.bar(r, sleep_eve, color=colors[0], edgecolor='white', width=barWidth, label="sleep")
	plt.bar(r, awake_day, bottom=np.array(sleep_eve), color=colors[2], edgecolor='white', width=barWidth, label='awake')
	plt.bar(r, sleep_morn, bottom=np.array(sleep_eve) + np.array(awake_day), color=colors[0], edgecolor='white', width=barWidth)
	plt.bar(r, awake_morn, bottom=np.array(sleep_eve) + np.array(awake_day) + np.array(sleep_morn), color=colors[2], edgecolor='white', width=barWidth)
	
	# Increasing time on y axis
	# plt.bar(r, awake_morn, color=colors[2], edgecolor='white', width=barWidth, label="awake")
	# plt.bar(r, sleep_morn, bottom=np.array(awake_morn), color=colors[0], edgecolor='white', width=barWidth, label='sleep')
	# plt.bar(r, awake_day, bottom=np.array(awake_morn) + np.array(sleep_morn), color=colors[2], edgecolor='white', width=barWidth)
	# plt.bar(r, sleep_eve, bottom=np.array(awake_morn) + np.array(sleep_morn) + np.array(awake_day), color=colors[0], edgecolor='white', width=barWidth)
	
	plt.legend()
	plt.show()


def main():
	days = []

	with open('quantified_self_2020_data.csv') as csvfile:
	    reader = csv.reader(csvfile)
	    for i, row in enumerate(reader):
	    	if i == 0 or i == 1:
	    		continue
	    	day = {
	    		"date": parse_date(row[0]),
	    		"date_str": row[0],
	    		"wake": parse_time(row[1]),
	    		"wake_str": row[1],
	    		"sleep": parse_time(row[2]),
	    		"sleep_str": row[2],
	    	}

	        days.append(day)

	data = format_data(days)
	# plt_bar(data)

	df = to_data_frame(data)
	# exit()
	plotly_bar(df)

if __name__ == "__main__":
	main()
