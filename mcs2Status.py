import logging

class controllerStatus:
    def __init__(self, channel) -> None:
        self.chan = channel
        pass
    
    def status_is_referencing(self, status):
        status = int(status)
        is_referencing = int ('8',16)
        result = (status & is_referencing)
        if (result) == (is_referencing):
            return 1
        else:
            return 0

    def status_is_moving(self, status):
        status = int(status)
        move_active = int ('1',16)
        result = (status & move_active)
        if (result) == (move_active):
            return 1
        else:
            return 0
    
    def status_is_enabled(self, status):
        status = int(status)
        is_enabled = int ('40000',16)
        result = (status & is_enabled)
        if int(result) == is_enabled:
            logging.info("Axis enabled")
            return 1
        else:
            logging.info("Axis disabled")
            return 0
    
    def status_end_stop_reached(self, status):
        status = int(status)
        end_stop = int ('100',16)
        result = (status & end_stop)
        if (result) == (end_stop):
            return 1
        else:
            return 0

    def status_is_referenced(self, status):
        status = int(status)
        is_referenced = int ('80',16)
        result = (status & is_referenced)
        if (result) == (is_referenced):
            return 1
        else:
            return 0


