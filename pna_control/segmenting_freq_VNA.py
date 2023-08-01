#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyvisa
import time

# Replace 'YOUR_VNA_ADDRESS' with the address of your Rohde and Schwarz ZNA VNA, e.g., 'TCPIP0::192.168.1.100::inst0::INSTR'
vna_address = 'YOUR_VNA_ADDRESS'

# Open the VNA connection
rm = pyvisa.ResourceManager()
vna = rm.open_resource(vna_address)

# Frequency range and segment settings
start_freq = 1e9     # Start frequency in Hz
stop_freq = 6e9      # Stop frequency in Hz
num_segments = 5     # Number of segments to divide the frequency range

# Define the number of data points for each segment (modify as desired)
data_points_per_segment = [51, 61, 41, 71, 37]

# Configure the total number of data points for the entire frequency range
total_data_points = sum(data_points_per_segment)
vna.write(f':SENS1:SWE:POIN {total_data_points}')

# Sweep settings for each segment
current_data_point = 0
for segment in range(num_segments):
    # Get the number of data points for the current segment
    segment_data_points = data_points_per_segment[segment]

    # Calculate the start and stop frequencies for the current segment
    segment_start_freq = start_freq + (segment * (stop_freq - start_freq) / num_segments)
    segment_stop_freq = start_freq + ((segment + 1) * (stop_freq - start_freq) / num_segments)

    # Configure the frequency range and data points for the current segment
    vna.write(f':SENS1:FREQ:STAR {segment_start_freq}')
    vna.write(f':SENS1:FREQ:STOP {segment_stop_freq}')
    vna.write(f':SENS1:SWE:POIN {segment_data_points}')

    # Trigger a single sweep
    vna.write(':SENS1:SWE:MODE SING')

    # Wait for the sweep to complete
    while int(vna.query('*OPC?')) == 0:
        time.sleep(0.1)

    # Fetch the measurement data for the current segment
    vna.write(':CALC1:DATA:SNP? 1')  # Replace '1' with the desired measurement trace (e.g., '2', '3', etc.)
    data = vna.read_bytes()

    # Process the measurement data for the current segment as per your requirement

    # Update the current data point position for the next segment
    current_data_point += segment_data_points

# Close the VNA connection
vna.close()

