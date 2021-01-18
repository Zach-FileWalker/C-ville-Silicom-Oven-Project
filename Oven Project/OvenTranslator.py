# ############################################################################
# Author: Zach Rinehart                         Date last modified: 01/18/2021
# Property of Silicom Connectivity Solutions
# ############################################################################
# This is the overarching OvenTranslator class. I designed the code in this
# way so that if anyone wants to add another oven at some point, they only
# need to adapt the code and do some minor tweaking. Whoever does this would
# need to create a new oven translator class that inherits from this class
# (which the CvilleOvenTranslator class does) and redefine the methods so that
# the code can run the same methods. Whoever does this would also need to
# refactor the main file so that it uses the name of the new translator
# instead of CvilleOvenTranslator and do some minor feature compatibility
# tweaking. This adaptability is really the only purpose for this file/class.
# ############################################################################

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