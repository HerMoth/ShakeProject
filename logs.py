import os
import shutil

log_dir = "/opt/log/"

#gets the current date for the log file
from datetime import date 
today = date.today().strftime("%Y-%m-%d")

archive_dir = "/home/pi/shake_logs/" + today 

os.makedirs(archive_dir, exist_ok=True) 

for filename in os.listdir(log_dir):
    
    shutil.copy(os.path.join(log_dir, filename),
os.path.join(archive_dir, filename))
    
print("Logs have been archived to " , archive_dir)