import gps
import time

# Connect to the gpsd daemon
session = gps.gps(mode=gps.WATCH_ENABLE)

while True:
    try:
        # Fetch the next GPS report
        report = session.next()
        
        # Process the TPV (Time-Position-Velocity) report
        if report['class'] == 'TPV':
            time_str = report.get('time', 'n/a')
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
            print("│    Time:       {}                   │".format(time_str))
            print("│    Latitude:   {}                   │".format(lat))
            print("│    Longitude:  {}                   │".format(lon))
            print("│    Altitude:   {} m                 │".format(alt))
            print("│    Speed:      {} kph             │".format(speed))
            print("│    Heading:    {} deg (true)      │".format(track))
            print("│    Climb:      {} m/min           │".format(climb))
            print("│    Status:     {} ({:.3f} secs)│".format('3D FIX' if mode == 3 else '2D FIX' if mode == 2 else 'NO FIX', ept))
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


