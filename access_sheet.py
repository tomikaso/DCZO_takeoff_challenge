import pandas as pd
import ftplib
import constants

# Extract the unique sheet ID from your URL
sheet_id = constants.sheet_id  # gets the id of the google sheet;
takeoff_sheet = "takeoffs"
flight_sheet = "flights"

# Reformat the URL to request a CSV export
csv_url_takeoffs = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={takeoff_sheet}"
# csv_url_flights = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={flight_sheet}"

# map setup
zero_lat, zero_long = 47.390626, 8.480846

# Read into a Pandas DataFrame
df_takeoffs = pd.read_csv(csv_url_takeoffs)
# df_flights = pd.read_csv(csv_url_flights)

takeoffs = ''
row = 0
while row < len(df_takeoffs):
    lat = int((float(df_takeoffs['latitude'][row].replace(',', '.')) - zero_lat) * -1250)
    long = int((float(df_takeoffs['longitude'][row].replace(',', '.')) - zero_long) * 912)
    takeoffs = takeoffs + df_takeoffs['Startplatz'][row] + ',' + str(lat) + ',' + str(long) + ','
    row = row + 1
print(takeoffs)

# save takeoff-file
# path = ''  # test on windows
path = '/home/solarmanager/takeoff_challenge/' # for Raspi
takeoff_file = open(path + 'takeoffs.txt', 'w')
takeoff_file.write(takeoffs)
takeoff_file.close()
print("champion ranking created")

# send it to DCZO-webserver
session = ftplib.FTP('ftp.dczo.ch', constants.ftp_user, constants.ftp_pw)
file0 = open(path + 'takeoffs.txt', 'rb')  # file to send
session.storbinary('STOR takeoff_challenge/takeoffs.txt', file0)  # send the file
file0.close()  # close file and FTP
session.quit()
print("files sent to DCZO")