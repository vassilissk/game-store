import datetime
# from safe_schedule import SafeScheduler
import schedule
import time
from time import sleep
# import flagpy as fp
#
# import phonenumbers
# from phonenumbers import timezone, carrier, geocoder

# phonenumber = phonenumbers.parse("+380679231685")
# print(phonenumber)
# timeZone = timezone.time_zones_for_number(phonenumber)
#
# # It print the timezone of a phonenumber
# print(timeZone)
# # Getting carrier of a phone number
# Carrier = carrier.name_for_number(phonenumber, 'en')
#
# # Getting region information
# Region = geocoder.description_for_number(phonenumber, 'en')
#
# # Printing the carrier and region of a phone number
# print(Carrier)
# print(Region)
# # print(fp.get_country_list())
# ukr = fp.get_flag_img('Ukraine')
# ukr.show()
# print(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
a=datetime.datetime.now()
sleep(1)
b=datetime.datetime.now()
a_timedelta = datetime.timedelta(seconds=3)
print(type(a),b, b-a<a_timedelta)