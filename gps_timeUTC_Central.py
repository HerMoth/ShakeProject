import gps
import time
from datetime import datetime
import pytz

# Connect to the gpsd daemon
session = gps.gps(mode=gps.WATCH_ENABLE)

# Define the US/Central time zone
central_tz = pytz.timezone('US/Central')

while True:
    try:
        # Fetch the next GPS report
        report = session.next()
        
        # Process the TPV (Time-Position-Velocity) report
        if report.get('class') == 'TPV':
            utc_time_str = getattr(report, 'time', 'n/a')
            if utc_time_str != 'n/a':
                utc_time_obj = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                utc_time = utc_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                local_time = utc_time_obj.replace(tzinfo=pytz.utc).astimezone(central_tz)
                local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            else:
                utc_time = 'n/a'
                local_time_str = 'n/a'
            
            lat = getattr(report, 'lat', 'n/a')
            lon = getattr(report, 'lon', 'n/a')
            alt = getattr(report, 'alt', 'n/a')
            speed = getattr(report, 'speed', 'n/a')
            track = getattr(report, 'track', 'n/a')
            climb = getattr(report, 'climb', 'n/a')
            mode = getattr(report, 'mode', 'n/a')
            ept = getattr(report, 'ept', 'n/a')
            epv = getattr(report, 'epv', 'n/a')
            grid = 'EN50vc'  # Assuming a static grid square for this example
            
            # Print the TPV data
            print("┌───────────────────────────────────────────┐")
            print(f"│    UTC Time:   {utc_time}                   │")
            print(f"│    Local Time: {local_time_str}                   │")
            print(f"│    Latitude:   {lat}                   │")
            print(f"│    Longitude:  {lon}                   │")
            print(f"│    Altitude:   {alt} m                 │")
            print(f"│    Speed:      {speed} kph               │")
            print(f"│    Heading:    {track} deg (true)        │")
            print(f"│    Climb:      {climb} m/min             │")
            print(f"│    Status:     {'3D FIX' if mode == 3 else '2D FIX' if mode == 2 else 'NO FIX'} ({ept:.3f} secs)    │")
            print("│    Longitude Err:   n/a                │")
            print("│    Latitude Err:    n/a                │")
            print(f"│    Altitude Err:    +/- {epv} m        │")
            print("│    Course Err:      n/a                │")
            print("│    Speed Err:       n/a                │")
            print(f"│    Time offset:     {ept:.3f}              │")
            print(f"│    Grid Square:     {grid}             │")
            print("└───────────────────────────────────────────┘")
        
        # Process the SKY report for satellite information
        elif report.get('class') == 'SKY':
            satellites = getattr(report, 'satellites', [])
            print("┌─────────────────────────────────┐")
            print("│PRN:   Elev:  Azim:  SNR:  Used: │")
            for sat in satellites:
                prn = sat.get('PRN', 'n/a')
                elev = sat.get('el', 'n/a')
                azim = sat.get('az', 'n/a')
                snr = sat.get('ss', 'n/a')
                used = 'Y' if sat.get('used', False) else 'N'
                print(f"│ {prn: >3}    {elev: >2}    {azim: >3}    {snr: >2}      {used}   │")
            print("└─────────────────────────────────┘")
        
        time.sleep(1)

    except KeyError:
        pass
    except KeyboardInterrupt:
        break
    except StopIteration:
        session = None
        print("GPSD has terminated")
    except Exception as e:
        print(f"Unexpected error: {e}")
