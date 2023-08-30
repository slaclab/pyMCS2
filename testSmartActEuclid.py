from SmarAct2 import SmarActController2
from cbxfelCheckoutLog import cbxfelLog
from datetime import datetime
import logging
import json


stageSN = input("\nEnter serial number etched at the side of the stage. This will be the filename.\n")

now = datetime.now()
date_time = now.strftime("%m%d%Y_%H_%M")
file_name = 'logs/{}_{}.log'.format(stageSN, date_time)

#start the logger
logging.basicConfig(filename=file_name, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level= logging.INFO)
logging.info("BEGINNING TEST")
logging.info("Stage serial number: {}".format(stageSN))

cbxfelLog()

IP = "134.79.219.36"
units= 1000000000

print("\nIP: {}".format(IP))
logging.info("IP: {}\n".format(IP))

logging.info("Item 6:")
print("\nItem 6:")
chan = input("Enter controller channel (0/1/2): \n")
logging.info("Enter controller channel (0/1/2): {}".format(chan))

print("\nConfirm that the SmarAct Motion Control Software is configured to control the correct axis:")
msg = input("y or n: \n")
logging.info("Confirm that the SmarAct Motion Control Software is configured to control the correct axis:")
logging.info("y or n: {} \n".format(msg))

smart = SmarActController2(IP)
smart.create()
smart.connect()

print("\nSerial Number: {}".format(smart.get_serial_num()))
print("Positioner type Name: {}".format(smart.get_positioner_type_name(chan)))
print("Positioner reference type: {}".format(smart.get_positioner_reference_type(chan)))
smart.set_test_constraints(chan,units)
smart.get_test_constraints(chan,units)

logging.info("Item 7:")
print("\nItem 7:")
print("Confirm that the frequency, velocity, and acceleration parameters are consistent with the restrictions in Section 9.2 of this document.")
msg = input("y or n: \n")
logging.info("Confirm that the frequency, velocity, and acceleration parameters are consistent with the restrictions in Section 9.2 of this document.")
logging.info("y or n:{} \n".format(msg))

logging.info("Item 8:")
print("\nItem 8:")
print("Inital actuator position (mm): {}".format(smart.get_position(chan,units)))


logging.info("Item 9:")
print("\nItem 9:")
print("Command an incremental movement of 1.0 mm in positive direction")
logging.info("Command an incremental movement of 1.0 mm in positive direction")
msg = input("y or n: \n")
logging.info("y or n: {}\n".format(msg))

if msg == "y":
 smart.move_relative(1,chan,units,1)
 moveConfirmation =input("Confirm visually that the stage has moved by correct amount and in the correct direction (y/n): \n")
 logging.info("Confirm visually that the stage has moved by correct amount and in the correct direction (y/n): {}".format(moveConfirmation))
 
 moveDirection =input("Report direction of motion (p/n): \n")
 logging.info("Report direction of motion (p/n): {}".format(moveDirection))
else:
 print("Response was either n or skipped")
 logging.info("Response was either n or skipped")
 print("Cannot confirm visually that the stage has moved. \n")
 logging.info("Cannot confirm visually that the stage has moved. \n")
 print("Cannot report direction of motion. \n")
 logging.info("Cannot report direction of motion. \n")


print("Current position (mm): {}".format(smart.get_position(chan,units)))

logging.info("Item 10:")
print("\nItem 10:")
print("Command an incremental movement of 1.0 mm in negative direction")
logging.info("Command an incremental movement of 1.0 mm in negative direction")
msg = input("y or n: \n")
logging.info("y or n: {} \n".format(msg))

if msg == "y":
 smart.move_relative(1,chan,units,0)
 moveConfirmation =input("Confirm visually that the stage has moved by correct amount and in the correct direction (y/n): \n")
 logging.info("Confirm visually that the stage has moved by correct amount and in the correct direction (y/n): {}".format(moveConfirmation))
 moveDirection =input("Report direction of motion (p/n): \n")
 logging.info("Report direction of motion (p/n): {}".format(moveDirection))
else:
 print("Response was either n or skipped\n")
 logging.info("Response was either n or skipped\n")
 print("Cannot confirm visually that the stage has moved. \n")
 logging.info("Cannot confirm visually that the stage has moved. \n")
 print("Cannot report direction of motion. \n")
 logging.info("Cannot report direction of motion. \n")


print("Current position (mm): {}".format(smart.get_position(chan,units)))

logging.info("Item 11:")
print("\nItem 11:")
dirConfirmation =input("Are physical positive and negative directions of motion consistent with directions of motions defined in SLAC-I-120-005 (y/n): ")
logging.info("Are physical positive and negative directions of motion consistent with directions of motions defined in SLAC-I-120-005 (y/n): {}\n".format(dirConfirmation))

logging.info("Item 12:")
print("\nItem 12:")
logging.info("Axis will be homed in positive direction.\n" )
print("Axis will be homed in positive direction.\n" )

logging.info("Item 13:")
print("\nItem 13:")

findReference =input("Find Reference in default positive direction ? (y/n): \n")
logging.info("Find Reference in default positive direction ? (y/n): {}".format(findReference))
if findReference == "y":
 smart.find_reference(chan)
 print("Current position (mm): {}".format(smart.get_position(chan,units)))
 moveConfirmation =input("Confirm the stage has moved to correct end of travel and readback is 0. (y/n): \n")
 logging.info("Confirm the stage has moved to correct end of travel and readback is 0. (y/n): {}\n".format(moveConfirmation))
else:
 print("Skip finding reference")
 logging.info("Skip finding reference")
 print("Skip confirming the stage has moved to correct end of travel and readback is 0.\n")
 logging.info("Skip confirming the stage has moved to correct end of travel and readback is 0.\n")


logging.info("Item 14:")
print("\nItem 14:")

limit = input("Incrementally move the stage in positive end of the range of motion.(y/n): \n")
logging.info("Incrementally move the stage in positive end of the range of motion.(y/n): {}".format(limit))
if limit == "y":
 smart.find_limit(chan,"pos",units)
 limit1 = smart.get_position(chan,units)
 print("Current end of travel position (mm): {}".format(limit1))
 logging.info("Current end of travel position (mm): {}".format(limit1))
 skip = 0
else:
 print("Skipped moving to positive end of travel")
 logging.info("Skipped moving to positive end of travel")
 skip = 1

logging.info("\nItem 15:")
print("\nItem 15:")

limit = input("Incrementally move the stage in negative end of the range of motion.(y/n): \n")
logging.info("Incrementally move the stage in negative end of the range of motion.(y/n): {}".format(limit))
if limit == "y":
 smart.find_limit(chan,"neg",units)
 limit2 = smart.get_position(chan,units)
 print("Current end of travel position (mm): {}".format(limit2))
 logging.info("Current end of travel position (mm): {}".format(limit2))
 skip = 0
else:
 print("Skipped moving to negative end of travel")
 logging.info("Skipped moving to negative end of travel")
 skip = 1

logging.info("\nItem 16:")
print("\nItem 16:")

if skip != 1:
 msg = input("Incrementally move the stage to midpoint of the range of motion.(y/n): \n")
 logging.info("Incrementally move the stage to midpoint of the range of motion.(y/n): {}".format(msg))
 if msg == "y":
   totalTravel = abs(limit1) + abs(limit2)
   midTravel = totalTravel/2
   tweak = midTravel
   dirn = 1
   smart.move_relative(tweak,chan,units,dirn)
   print("Current position (mm): {}\n".format(smart.get_position(chan,units)))
   
 else:
   print("Skipped finding midpoint of travel range\n")
   logging.info("Skipped finding midpoint of travel range\n")

 logging.info("Item 17:")
 print("\nItem 17:")
 print("Difference in motor positions at limits to determine stage travel range (mm): {}".format(totalTravel))
 logging.info("Difference in motor positions at limits to determine stage travel range (mm): {}".format(totalTravel))

else:
 logging.info("Item 16 and 17:")
 print("\nItem 16 and 17:")
 print("As we did not move to both end of travel, we cannot find travel range or mid-point. END")  
 logging.info("As we did not move to both end of travel, we cannot find travel range or mid-point. END")  

smart.disconnect()


