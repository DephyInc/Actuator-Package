import os, sys
import glob
from time import sleep
import csv
import numpy as np
import sys
from scipy.signal import blackmanharris
from numpy.fft import rfft, irfft
from numpy import argmax, sqrt, mean, absolute, arange, log10

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.fxUtil import *

def rms_flat(a):
	"""Return the root mean square of all the elements of *a*, flattened out.
	
	"""
	return sqrt(mean(absolute(a)**2))

def find_range(f, x):
	"""Find range between nearest local minima from peak at index x
	
	"""
	lowermin = 0
	uppermin = 0
	for i in arange(x+1, len(f)):
		if f[i+1] >= f[i]:
			uppermin = i
			break
	for i in arange(x-1, 0, -1):
		if f[i] <= f[i-1]:
			lowermin = i + 1
			break
	return (lowermin, uppermin)

def THDN(signal, sample_rate):
	# Get rid of DC and window the signal
	signal -= mean(signal) # TODO: Do this in the frequency domain, and take any skirts with it
	windowed = signal * blackmanharris(len(signal))  # TODO Kaiser?
	# Measure the total signal before filtering but after windowing
	total_rms = rms_flat(windowed)

	# Find the peak of the frequency spectrum (fundamental frequency), and filter 
	# the signal by throwing away values between the nearest local minima
	f = rfft(windowed)
	i = argmax(abs(f))
	print('Frequency: %f Hz' % (sample_rate * (i / len(windowed)))) # Not exact
	lowermin, uppermin = find_range(abs(f), i)
	f[lowermin: uppermin] = 0

	# Transform noise back into the signal domain and measure it
	# TODO: Could probably calculate the RMS directly in the frequency domain instead
	noise = irfft(f)
	THDN = rms_flat(noise) / total_rms
	print("THD+N:     %.4f%% or %.1f dB" % (THDN * 100, 20 * log10(THDN)))

	plt.subplot(2, 2, 1)
	plt.plot(signal)
	plt.title("signal")

	plt.subplot(2, 2, 2)
	plt.title("windowed")
	plt.plot(windowed)

	plt.subplot(2, 2, 3)
	plt.title("noise")
	plt.plot(noise)

	plt.subplot(2, 2, 4)
	plt.title("FFT")
	plt.plot(f)

	plt.show()

def sineAnalyzer(data_log):
	timestamps = []
	sine_samples = []
	with open(data_log, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(f'Device data fields: {", ".join(row)}')
				line_count += 1
			timestamps.append(int(row["timestamp"]))
			sine_samples.append(int(row["accelx"]))
			line_count += 1
		print(f'Processed {line_count} lines.')
	start_time = timestamps[0]
	timestamps[:] = [time-start_time for time in timestamps[:]]
	sine_samples[:] = [sample-16384 for sample in sine_samples[:]]
	return timestamps, sine_samples

def fxCommunicationTester(port, baudRate, streaming_frequency = 500):
	# Connect to the Device Under Test (DUT)
	devId = fxOpen(port, baudRate, streaming_frequency, 0)
	# Print out the device ID
	print("Device ID: ", devId)
	# Command the device to start streaming data
	fxStartStreaming(devId, True)
	# Allow the device class to handle processing the streaming data in the background
	# this total will give us about two full waves based on 1000 samples per wave
	sleep(2000/streaming_frequency)
	# Close the device so it stops streaming and no longer writes to the csv file
	fxClose(devId)
	# Give a moment for the csv file to cleanly close
	sleep(1)
	# All test data is currently stored in the data logger csv file so can now be used for
	# communication quality analysis
	data_logs = glob.glob("Data*")
	last_log = data_logs[-1]
	print("Log file under analysis is ", last_log)
	timestamps, sine_samples = sineAnalyzer(last_log)
	print("received ", len(timestamps), " samples")
	THDN(sine_samples, streaming_frequency)

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxCommunicationTester(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
