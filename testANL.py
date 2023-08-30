from SmarAct2 import SmarActController2
#import cbxfelTestLogConst
from datetime import datetime
import logging

tester = input("Tester Name and Initials: \n")

print("Select test schedule phase:")
print("1:Pre-bakeout")
print("2:Pre-shipment")
print("3:Pre-installation")
print("4:Post-installation")
testSch = input("Select from 1 to 4: \n")

print("Select test location:")
print("1:ANL Lab/Workshop")
print("2:SLAC Lab/Workshop")
print("3:Undulator Hall")
testLoc = input("Select from 1 to 3: \n")

print("Select station ID:")
print("1:C")
print("2:D")
statID = input("Select from 1 or 2: \n")

if statID == "1":
  print("Select component ID:")
  print("1:X24")
  compID = input("Select from 1: \n")
    
if statID == "2":
  print("Select component ID:")
  print("1:X23")
  print("2:X23G")
  print("3:X24E")
  compID = input("Select from 1 to 3: \n")

print("Select axis ID:")
print("1:X")
print("2:Y")
axisID = input("Select from 1 or 2: \n")

stageSN = input("Enter serial number etched at the side of the stage: \n")

chan = input("Enter controller channel: \n")

now = datetime.now()

IP = input("Enter IP: \n")
units= 1000000000
 
date_time = now.strftime("%m%d%Y_%H_%M")
file_name = 'logs/{}_{}.log'.format(stageSN, date_time)

#start the logger
logging.basicConfig(filename=file_name, filemode='w', format='%(name)s - %(levelname)s - %(message)s', level= logging.INFO)
logging.info("BEGINNING TEST")
logging.info("Test location: {}".format(testLoca))
logging.info("Station ID: {}".format(stationID))
logging.info("Axis ID: {}".format(axisID))
logging.info("Stage serial number: {}".format(stageSN))
logging.info("Date: {}, Time: {}".format(now.strftime("%m/%d/%Y"), now.strftime("%H:%M:%S")))
logging.info("\n")

smart = SmarActController2(IP)
smart.create()
smart.connect()
print("Serial Number: {}".format(smart.get_serial_num()))
print("Positioner type Name: {}".format(smart.get_positioner_type_name(chan)))
print("Positioner reference type: {}".format(smart.get_positioner_reference_type(chan)))
smart.set_test_constraints(chan,units)
print("Max closed loop frequency (Hz): {}".format(smart.get_max_closed_loop_freq(chan)))
print("Positioner velocity (mm/sec): {}".format(smart.get_velocity(chan,units)))
print("Positioner acceleration (mm/sec2): {}".format(smart.get_acceleration(chan,units)))
print("Current position (mm): {}".format(smart.get_position(chan,units)))

dirnText = input("Move direction [Relative] (pos/neg): \n")
tweak = input("Move the axis by (mm) [Relative]: \n")

if dirnText == "pos":
 dirn = 1
if dirnText == "neg":
 dirn = 0
print(f'direction text = {dirnText} and dirn = {dirn}')

smart.move_relative(tweak,chan,units,dirn)
print("Current position (mm): {}".format(smart.get_position(chan,units)))
moveConfirmation =input("Confirm visually that the stage has moved (yes/no): \n")

logging.info("Confirm visually that the stage has moved (yes/no): {}".format(moveConfirmation))

moveDirection =input("Confirm direction of motion (pos/neg): \n")
logging.info("Confirm direction of motion (pos/neg): {}".format(moveDirection))

dirnText = input("Move direction [Relative] (pos/neg ): \n")
tweak = input("Move the axis by (mm) [Relative]: \n")
if dirnText == "pos":
 dirn = 1
if dirnText == "neg":
 dirn = 0
smart.move_relative(tweak,chan,units,dirn)

print("Current position (mm): {}".format(smart.get_position(chan,units)))

moveConfirmation =input("Confirm visually that the stage has moved (yes/no): \n")
logging.info("Confirm visually that the stage has moved (yes/no): {}".format(moveConfirmation))

moveDirection =input("Confirm direction of motion (pos/neg): \n")
logging.info("Confirm direction of motion (pos/neg): {}".format(moveDirection))

dirConfirmation =input("Are physical positive and negative directions of motion consistent with definitions (yes/no): \n")
logging.info("Are physical positive and negative directions of motion consistent with definitions (yes/no): {}".format(dirConfirmation))

findReference =input("Find Reference ? (yes/no): \n")
if findReference == "yes":
 smart.find_reference(chan)
else:
 print("Skip finding reference")

print("Current position (mm): {}".format(smart.get_position(chan,units)))

tweak = input("Move the axis to (mm) [Absolute]: \n")
smart.move_absolute(chan,tweak,units)
print("Current position (mm): {}".format(smart.get_position(chan,units)))

tweak = input("Move the axis to (mm) [Absolute]: \n")
smart.move_absolute(chan,tweak,units)
print("Current position (mm): {}".format(smart.get_position(chan,units)))

limit = input("Find Limit (pos/neg): \n")
smart.find_limit(chan,limit,units)
limit1 = smart.get_position(chan,units)
print("Current end of travel position (mm): {}".format(limit1))
logging.info("Current end of travel position (mm): {}".format(limit1))
limit = input("Find Limit (pos/neg): \n")
smart.find_limit(chan,limit,units)
limit2 = smart.get_position(chan,units)
print("Current end of travel position (mm): {}".format(limit2))
logging.info("Current end of travel position (mm): {}".format(limit2))
totalTravel = abs(limit1) + abs(limit2)
print("Total Range (mm): {}".format(totalTravel))
logging.info("Total Range (mm): {}".format(totalTravel))
midTravel = totalTravel/2
if limit == "pos":
 tweak = midTravel
 dirn = 0
if limit == "neg":
 tweak = midTravel
 dirn = 1
print("Moving Axis to mid point by (mm): {}".format(tweak))
logging.info("Moving Axis to mid point by (mm): {}".format(tweak))
smart.move_relative(tweak,chan,units,dirn)
print("Current position (mm): {}".format(smart.get_position(chan,units)))

smart.disconnect()

