import datetime
# from safe_schedule import SafeScheduler
import schedule
import time
from time import sleep

q = datetime.datetime.now()
sleep(2)
w = datetime.datetime.now()
print((w - q) < datetime.timedelta(seconds=3))


def job():
    print("Работаю")
schedule.every(3).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)