from abc import ABC, abstractmethod

class OvenTranslator(ABC):

    # serial connection with oven
    global oven

    # Is the temp param within reasonable bounds (Celsius)?
    # Concrete
    def isAcceptableTemp(self, temp: float):

        if -50 <= temp <= 90:
            return True
        else:
            return False

    # Turn oven on
    # Abstract
    def setTemp(self, temp):
        pass

    # Get the current temp of the oven
    # Abstract
    def getTemp(self):
        pass