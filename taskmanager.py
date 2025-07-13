import schedule
import time 

a = 1
def greet():
	print('hey hello this is the schedule function ')
	print('logging time : ',time.strftime('%H:%M:%S'))
	a+=1

schedule.every().minutes.do(greet)

while True:
	if a ==2:
		break
	schedule.run_pending()
	time.sleep(1)
