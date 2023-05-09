import ftplib
import os
from datetime import datetime, timedelta

pfx='Jefferson'
eq='daily'

def update_last_send(date):
	with open("C:\ptlspg\last_date.txt", "w") as f:
		f.write(date)

def connect_to_ftp_server():
	try:
		session = ftplib.FTP("70.88.80.197","Intellimeter","Reads123")
		session.cwd("/Intellimeter/PresidentialCity/PresidentialCity(Jefferson)")
		#print("Connected to FTP server")
		return session
	except Exception as e:
		print(f"Failed to connect to Server. Due: {e}")
		
def send_file(session, filename, date):
	file = open(filename, 'rb')
	#print(f"Uploading File {filename} to Server")
	try:
		session.storbinary("STOR " + os.path.basename(filename), file)
		print(f"{filename} sended successfully")
		update_last_send(date)
	except Exception as e:
		print(f"An error ocurred: {e}")
		exit()
	
	file.close()
	
def main():
	with open("C:\ptlspg\last_date.txt") as f:
		date = f.readlines()
    
	previous_date = datetime.strptime(date[0],"%Y-%m-%d")
	today = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
	#print(today)
	while previous_date < today:
		new_date = previous_date + timedelta(days=1)
		new_date_str = datetime.strftime(new_date, "%Y-%m-%d")
		date_name = datetime.strftime(new_date, "%Y%m%d")
		filename = "C:\ptlspg\csv\\" + pfx + "_" + eq + "_" + date_name + ".csv"
		
		#print(previous_date, new_date, filename)
		
		session = connect_to_ftp_server()
		send_file(session, filename, new_date_str)
		previous_date = previous_date + timedelta(days=1)
		session.quit()
		
main()