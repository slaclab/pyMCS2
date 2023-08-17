import socket
import time
import logging
from mcs2Status import controllerStatus

class SmarActController2:
    def __init__(self, dev_ip) -> None:
        self.ip = dev_ip
        self.client = None
        pass
    
    def create(self):
        try:
            logging.info("Creating socket for {} port".format(self.ip))
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            timeout_seconds = 30
            self.client.settimeout(timeout_seconds)
            logging.info("Socket created.")
        except Exception as e:
            print("Failed to create socket")
            logging.critical("Failed to create socket: " + str(e))
            raise Exception("Failed to create socket: " + str(e))
        return None

    def connect(self):
        try:
            logging.info("Connecting to {} port".format(self.ip))
            self.client.connect((self.ip,55551))
            logging.info("Connected to {}".format(self.ip))
        except Exception as e:
            print("Unable to connect")
            logging.critical("Unable to connect: " + str(e))
            raise Exception("Unable to connect: " + str(e))
        return None

    def disconnect(self):
        self.client.close()
        logging.info("Disconnected to {}".format(self.ip))
    
    def send_no_response(self,command):
        self.client.send(bytes(command+'\r\n','ascii'))

    def send(self,command):
        self.client.send(bytes(command+'\r\n','ascii'))
        try:
            msg = self.client.recv(1024).decode('ascii')
        except Exception as e:
            print("No Response. Timeout")
            logging.critical("No Response. Timeout: " + str(e))
            raise Exception("No Response. Timeout: " + str(e))
        return msg
    
    def get_serial_num(self):
        msg = self.send(":DEV:SNUM?")
        logging.info("Get serial number: {}". format(msg))
        return msg

    def get_sensor_type(self):
        msg = self.send(":DEV:PTYP?")
        logging.info("Get sensor type: {}". format(msg))
        return msg

    def get_positioner_type_name(self,channel:int):
        msg = self.send(":CHAN{}:PTYP:NAME?".format(channel))
        logging.info("Get positioner type name: {}". format(msg))
        return msg

    def get_position(self,channel:int,units: int):
        msg = self.send(":CHAN{}:POS:CURR?".format(channel))
        logging.info("Current position (units): {}". format(msg))
        posn = int(msg)/units
        logging.info("Current position (mm): {}". format(posn))
        return posn

    def get_max_closed_loop_freq(self,channel:int):
        msg = self.send(":CHAN{}:MCLF?".format(channel))
        logging.info("Max Closed Loop Frequency (Hz): {}". format(msg))
        return msg

    def get_positioner_reference_type(self,channel:int):
        msg = self.send(":CHAN{}:TUN:RTYP?".format(channel))
        if int(msg) == 0:
            logging.info("Positoner reference type: None")
        elif int(msg) == 1:
         logging.info("Positoner reference type: Hard Stop")
        elif int(msg) == 2:
         logging.info("Positoner reference type: Single Coded")
        elif int(msg) == 3:
         logging.info("Positoner reference type: Distance Coded")
        else: 
            logging.info("Error in querying positioner reference")
        return msg

    def get_velocity(self,channel:int,units: int):
        msg = self.send(":CHAN{}:VEL?".format(channel))
        logging.info("Positoner velocity (units/sec): {}". format(msg))
        velo = int(msg)/units
        logging.info("Positoner velocity (mm/sec): {}". format(velo))
        return (velo)

    def get_acceleration(self,channel:int,units: int):
        msg = self.send(":CHAN{}:ACC?".format(channel))
        logging.info("Positoner acceleration (units/sec2): {}". format(msg))
        accl = int(msg)/units
        logging.info("Positoner acceleration (mm/sec2): {}". format(accl))
        return (accl)

    def move_absolute(self,channel:int,position: int, units: int):
        timeout = 240
        time_elapsed = []
        status = self.get_status("{}".format(channel))
        mcs2 = controllerStatus(channel)
        if not mcs2.status_is_enabled(status):
           print("Amplifier not enabled. Enabling now")
           self.send_no_response(":CHAN{}:AMPL:ENAB 1".format(channel))
        timeout_elapsed = False
        self.send_no_response(":CHAN{}:MMODE 0".format(channel))
        logging.info("Move to position: {}". format(position))
        position = int(position)*units
        start_time = time.time()
        self.send_no_response(":MOVE{} {}".format(channel,position))
        time.sleep(0.1)
        status = self.get_status("{}".format(channel))
        while not timeout_elapsed :
            time.sleep(0.1)
            status = self.get_status("{}".format(channel))
            if not mcs2.status_is_moving(status):
               print("Move complete.")
               logging.info("Axis move complete")
               timeout_elapsed = True
            if (time.time()-start_time) > timeout:
                logging.info("Channel {} polling timeout elapsed ({}s)". format(channel, timeout))
                timeout_elapsed = True
                print("Timeout Elapsed")
        status = self.get_status("{}".format(channel))
        if mcs2.status_end_stop_reached(status):
           logging.info("Hard stop reached")

    def find_limit(self,channel:int,direction, units: int):
        timeout = 240
        time_elapsed = []
        status = self.get_status("{}".format(channel))
        mcs2 = controllerStatus(channel)
        if not mcs2.status_is_enabled(status):
           print("Amplifier not enabled. Enabling now")
           self.send_no_response(":CHAN{}:AMPL:ENAB 1".format(channel))
        timeout_elapsed = False
        self.send_no_response(":CHAN{}:MMODE 0".format(channel))
        logging.info("Move to find {} limit". format(direction))
        if direction == "pos":
         position = 30*units
        if direction == "neg":
         position = -30*units
        start_time = time.time()
        self.send_no_response(":MOVE{} {}".format(channel,position))
        time.sleep(0.1)
        status = self.get_status("{}".format(channel))
        while not timeout_elapsed :
            time.sleep(0.1)
            status = self.get_status("{}".format(channel))
            if not mcs2.status_is_moving(status):
               print("Move complete.")
               logging.info("Axis move complete")
               timeout_elapsed = True
            if (time.time()-start_time) > timeout:
                logging.info("Channel {} polling timeout elapsed ({}s)". format(channel, timeout))
                timeout_elapsed = True
                print("Timeout Elapsed")
        status = self.get_status("{}".format(channel))
        if mcs2.status_end_stop_reached(status):
           print("Reached hard stop.")
           logging.info("Hard stop reached")
 
    def move_relative(self,tweak: int,channel:int,units: int,dirn):
        timeout = 300
        time_elapsed = []
        status = self.get_status("{}".format(channel))
        mcs2 = controllerStatus(channel)
        if not mcs2.status_is_enabled(status):
           print("Amplifier not enabled. Enabling now")
           self.send_no_response(":CHAN{}:AMPL:ENAB 1".format(channel))
        timeout_elapsed = False
        self.send_no_response(":CHAN{}:MMODE 1".format(channel))
        start_time = time.time()
        if dirn == 1:
           logging.info("Move in positive direction in mm by {}". format(tweak))
           posn = int(tweak)*units
        else:
           logging.info("Move in negative direction in mm by {}". format(tweak))
           posn = int(tweak)*units*(-1)
           
        self.send_no_response(":MOVE{} {}".format(channel,posn))
        time.sleep(0.1)
        status = self.get_status("{}".format(channel))
        while not timeout_elapsed :
            time.sleep(0.1)
            status = self.get_status("{}".format(channel))
            if not mcs2.status_is_moving(status):
               print("Move complete.")
               logging.info("Axis move complete")
               timeout_elapsed = True
            if (time.time()-start_time) > timeout:
                logging.info("Channel {} polling timeout elapsed ({}s)". format(channel, timeout))
                timeout_elapsed = True
                print("Timeout Elapsed")
        status = self.get_status("{}".format(channel))
        if mcs2.status_end_stop_reached(status):
           print("Reached hard stop.")
           logging.info("Hard stop reached")

    def find_reference(self,channel:int):
        timeout = 240
        time_elapsed = []
        status = self.get_status("{}".format(channel))
        mcs2 = controllerStatus(channel)
        if not mcs2.status_is_enabled(status):
           print("Amplifier not enabled. Enabling now")
           self.send_no_response(":CHAN{}:AMPL:ENAB 1".format(channel))
        if mcs2.status_is_referenced(status):
           findReference =input("Axis referenced. Find Reference again? (yes/no): \n")
        else:
           findReference = "yes"
        if findReference == "yes":
              self.send_no_response(":CHAN{}:REF:OPT 0".format(channel))
              logging.info("Setting ref option to stop at reference mark and set value to 0.")
              self.send_no_response(":REF{}".format(channel))
              timeout_elapsed = False
              start_time = time.time()
              status = self.get_status("{}".format(channel))
              while not timeout_elapsed :
                  time.sleep(0.1)
                  status = self.get_status("{}".format(channel))
                  if not mcs2.status_is_referencing(status):
                     print("Referencing complete.")
                     logging.info("Axis referencing complete")
                     timeout_elapsed = True
                  if (time.time()-start_time) > timeout:
                      logging.info("Axis {} polling timeout elapsed ({}s)". format(channel, timeout))
                      timeout_elapsed = True
                      print("Timeout Elapsed")
              print("Referencing complete")
        else:
              print("Skip finding reference")
        time.sleep(0.1)
        status = self.get_status("{}".format(channel))
        if mcs2.status_end_stop_reached(status):
           print("Reached hard stop.")
           logging.info("Hard stop reached")
        if mcs2.status_is_referenced(status):
           print("Axis referenced.")
           logging.info("Axis referenced")

    def set_test_constraints(self,channel:int,units: int):
        velo = 0.2 * units
        accl = 0.1 * units
        self.send_no_response(":CHAN{}:MCLF 100".format(channel))
        self.send_no_response(":CHAN{}:VEL {}".format(channel,velo))
        self.send_no_response(":CHAN{}:ACC {}".format(channel,accl))
        logging.info("Test Constraints set.")
        print("Test Constraints set.")

    def get_status(self, channel:int):
        msg = self.send(":CHAN{}:STAT?".format(channel))
        mcs2 = controllerStatus(channel)
        return msg


