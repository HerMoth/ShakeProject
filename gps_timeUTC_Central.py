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
        if report['class'] == 'TPV':
            utc_time_str = report.get('time', 'n/a')
            if utc_time_str != 'n/a':
                utc_time_obj = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                utc_time = utc_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                local_time = utc_time_obj.replace(tzinfo=pytz.utc).astimezone(central_tz)
                local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            else:
                utc_time = 'n/a'
                local_time_str = 'n/a'
            
            lat = report.get('lat', 'n/a')
            lon = report.get('lon', 'n/a')
            alt = report.get('alt', 'n/a')
            speed = report.get('speed', 'n/a')
            track = report.get('track', 'n/a')
            climb = report.get('climb', 'n/a')
            mode = report.get('mode', 'n/a')
            ept = report.get('ept', 'n/a')
            epv = report.get('epv', 'n/a')
            grid = 'EN50vc'  # Assuming a static grid square for this example
            
            # Print the TPV data
            print("┌───────────────────────────────────────────┐")
            print("│    UTC Time:   {}                   │".format(utc_time))
            print("│    Local Time: {}                   │".format(local_time_str))
            print("│    Latitude:   {}                   │".format(lat))
            print("│    Longitude:  {}                   │".format(lon))
            print("│    Altitude:   {} m                 │".format(alt))
            print("│    Speed:      {} kph               │".format(speed))
            print("│    Heading:    {} deg (true)        │".format(track))
            print("│    Climb:      {} m/min             │".format(climb))
            print("│    Status:     {} ({:.3f} secs)    │".format('3D FIX' if mode == 3 else '2D FIX' if mode == 2 else 'NO FIX', ept))
            print("│    Longitude Err:   n/a                │")
            print("│    Latitude Err:    n/a                │")
            print("│    Altitude Err:    +/- {} m        │".format(epv))
            print("│    Course Err:      n/a                │")
            print("│    Speed Err:       n/a                │")
            print("│    Time offset:     {:.3f}              │".format(ept))
            print("│    Grid Square:     {}             │".format(grid))
            print("└───────────────────────────────────────────┘")
        
        # Process the SKY report for satellite information
        elif report['class'] == 'SKY':
            satellites = report.get('satellites', [])
            print("┌─────────────────────────────────┐")
            print("│PRN:   Elev:  Azim:  SNR:  Used: │")
            for sat in satellites:
                prn = sat.get('PRN', 'n/a')
                elev = sat.get('el', 'n/a')
                azim = sat.get('az', 'n/a')
                snr = sat.get('ss', 'n/a')
                used = 'Y' if sat.get('used', False) else 'N'
                print("│ {: >3}    {: >2}    {: >3}    {: >2}      {}   │".format(prn, elev, azim, snr, used))
            print("└─────────────────────────────────┘")
        
        time.sleep(1)

    except KeyError:
        pass
    except KeyboardInterrupt:
        break
    except StopIteration:
        session = None
        print("GPSD has terminated")
