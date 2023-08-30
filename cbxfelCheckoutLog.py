import logging
from datetime import datetime

test_schedule = {
    "1":"Pre Bakeout",
    "2":"Pre Shipment",
    "3":"Pre Installation",
    "4":"Post Intallation"
}

test_loca =  {
    "1":"ANL Lab/Workshop",
    "2":"SLAC Lab/Workshop",
    "3":"Undulator Hall"
}

stat_ID = {
    "1":"C",
    "2":"D"
}

component_ID_C = {
    "1":"X23", 
    "2":"X23G",
    "3":"X23E"
}

component_ID_D = {
    "1":"X24"
}

axis_ID = {
    "1":"X",
    "2":"Y"
}

class cbxfelLog:
   def __init__(self):
       cbxfelLog.tester_info()

       print("\nSelect test location:")
       print("1:ANL Lab/Workshop")
       print("2:SLAC Lab/Workshop")
       print("3:Undulator Hall")
       testLoca = input("Enter 1 or 2 or 3: \n")
       cbxfelLog.test_location(testLoca)

       logging.info("Item 1:")
       print("\nItem 1:")
       print("Select test schedule phase:")
       print("1:Pre-bakeout")
       print("2:Pre-shipment")
       print("3:Pre-installation")
       print("4:Post-installation")
       testSch = input("Enter 1 or 2 or 3 or 4: \n")
       cbxfelLog.test_schedule_phase(testSch)

       logging.info("Item 2:")
       print("\nItem 2:")
       print("Select station ID:")
       print("1:C")
       print("2:D")
       statID = input("Enter 1 or 2: \n")
       cbxfelLog.station_ID(statID)

       logging.info("Item 3:")
       print("\nItem 3:")
       cbxfelLog.component_ID(statID)

       logging.info("Item 4:")
       print("\nItem 4:")
       print("Select axis ID:")
       print("1:X")
       print("2:Y")
       axisID = input("Enter 1 or 2: \n")
       cbxfelLog.axis_xy_ID(axisID)
       
       logging.info("Item 5:")
       print("\nItem 5:")
       print("Confirm the controller channel that this axis is assigned to in SLAC-I-120-174 matches the physical connection:")
       msg = input("y or n: \n")
       logging.info("Confirm the controller channel that this axis is assigned to in SLAC-I-120-174 matches the physical connection:")
       logging.info("y or n: {}\n".format(msg))

   def tester_info():
      tester = input("\nTester Name and Initials: \n")
      logging.info("Tester Name and Initials: {}".format(tester))
      now = datetime.now()
      logging.info("Date: {}, Time: {}".format(now.strftime("%m/%d/%Y"), now.strftime("%H:%M:%S")))
          
   def test_schedule_phase(msg):
      try:
         print("Test Schedule Phase: ",test_schedule[msg])
         logging.info("Test Schedule Phase: {}\n".format(test_schedule[msg]))
      except KeyError:
         logging.error("Invalid Test Schedule Phase: {}".format(msg))
         logging.error("Enter 1 or 2 or 3 or 4")
         print("Invalid Test Schedule Phase: ",msg)
         testSch = input("Enter 1 or 2 or 3 or 4: \n")
         cbxfelLog.test_schedule_phase(testSch)

   def test_location(msg):
      try:
         print("Test Location: ",test_loca[msg])
         logging.info("Test Location: {} \n".format(test_loca[msg]))
      except KeyError:
         logging.error("Invalid Test Location: {}".format(msg))
         logging.error("Enter 1 or 2 or 3")
         print("Invalid Test Location: ",msg)
         testLoca = input("Enter 1 or 2 or 3: \n")
         cbxfelLog.test_location(testLoca)

   def station_ID(msg):
      try:
         print("Station ID: ",stat_ID[msg])
         logging.info("Station ID: {}\n".format(stat_ID[msg]))
      except KeyError:
         logging.error("Invalid station ID: {}".format(msg))
         logging.error("Enter 1 or 2")
         print("Invalid station ID: ",msg)
         statID = input("Enter 1 or 2: \n")
         cbxfelLog.station_ID(statID)

   def component_ID(msg):
      if msg == "2":
        cID = component_ID_D['1']
        print("\nComponent ID: ",cID)
        logging.info("Component ID: {}\n".format(cID))
      else:
        print("\nSelect component ID:")
        print("1:X23")
        print("2:X23G")
        print("3:X23E")
        compID = input("Select from 1 to 3: \n")
        cID = component_ID_C[compID]
        try:
           print("Component ID: ",cID)
           logging.info("Component ID: {}\n".format(cID))
        except KeyError:
           logging.error("Invalid component ID: {}".format(compID))
           logging.error("Enter 1 or 2 or 3")
           print("Invalid component ID: ",compID)

   def axis_xy_ID(msg):
      try:
         print("Axis ID: ",axis_ID[msg])
         logging.info("Axis ID: {}\n".format(axis_ID[msg]))
      except KeyError:
         logging.error("Invalid axis ID: {}".format(msg))
         logging.error("Enter 1 or 2")
         print("Invalid axis ID: ",msg)
         axisID = input("Enter 1 or 2: \n")
         cbxfelLog.axis_xy_ID(axisID)

