import datetime
# from safe_schedule import SafeScheduler
import schedule
import time
from time import sleep
# import flagpy as fp
#
import phonenumbers
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
# Parsing String to Phone number
phone_number = phonenumbers.parse("+38 (067) 456 78 90")

# Validating a phone number
valid = phonenumbers.is_valid_number(phone_number)

# Checking possibility of a number
possible = phonenumbers.is_possible_number(phone_number)

# Printing the output
print(valid)
print(possible)
# a=[1,22,3,3,5,6,4,5,6,9]
# result = [a[i:i+3] for i in range(0, len(a), 3)]
#
# print(result)