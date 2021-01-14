from OvenTranslator import OvenTranslator
from telnetlib import Telnet
from time import sleep
from sys import exit


class CvilleOvenTranslator(OvenTranslator):

    # tests if oven online by doing Telnet handshake with remote server
    def __init__(self):
        try:
            tester = Telnet("172.24.0.7")
            tester.close()
        except:
            print("Couldn't handshake with oven")
            print("Oven appears to be offline")
            sleep(5)
            exit("Telnet test failed")

    # method to load compatible settings to oven that makes OPUS run better
    def load_default_settings(self):
        # setup
        for x in range(6):
            server = Telnet("172.24.0.7")
            sleep(0.1)
            server.write(b"= HYS2 0.4\n")
            sleep(0.1)
            server.write(b"= PB1 4.0\n")
            sleep(0.1)
            server.write(b"= PB2 0\n")
            sleep(0.1)
            server.write(b"= RE1 0.40\n")
            sleep(0.1)
            server.write(b"= RA1 0.00\n")
            sleep(0.1)
            server.write(b"= CT1 5\n")
            sleep(0.1)
            server.write(b"= DB 0.0\n")
            sleep(0.1)
            server.write(b"= CAL 0.0\n")
            sleep(0.1)
            server.write(b"= AUT 0\n")
            sleep(0.1)
            server.write(b"= C_F C\n")
            sleep(0.1)
            server.write(b"= RL -73.4\n")
            sleep(0.1)
            server.write(b"= RH 200.0\n")
            sleep(0.1)
            server.write(b"= PB1 4.0\n")
            sleep(0.1)
            server.close()

    # helper method to getTemp_sub
    def is_float(self, value):
        try:
            float(value)
            return True
        except:
            return False

    # get the temperature of the oven--base method
    def getTemp_sub(self):
        finalval = 0
        inputs = []

        # get inputs
        for i in range(2):
            float_input = ""

            # while decoded_input is not a float
            while not self.is_float(float_input):
                float_input = ""        # reset

                # setup
                server = Telnet("172.24.0.7")
                server.write(b"? C1\n")
                raw_input = server.read_until(b"\r")
                decoded_input = raw_input.decode("ascii")

                # input converter
                for char in decoded_input:
                    if char.isdigit() or char == "." or char == "-":
                        float_input += char

                # DEBUG
                if len(float_input) > 4 or not self.is_float(float_input):
                    print("DEBUG: CAUGHT INVALID VALUE: " + str(float_input))

                server.close()

            inputs.append(float(float_input))

        # compare two sample temps for erroneous temp reading
        if abs(inputs[0] - inputs[1]) < 1:
            finalval = inputs[0]

        # else run again recursively to get valid temp
        else:
            print("DEBUG: Recursive Breakpoint")
            print("DEBUG: Former: " + str(inputs[0]) + " and " + str(inputs[1]))
            finalval = self.getTemp()
            print("DEBUG: Finalval: " + str(finalval))

        return finalval

    # get the temperature of the oven--error handling with recursive to getTemp_sub
    def getTemp(self):
        try:
            return self.getTemp_sub()
        except KeyboardInterrupt:
            print("There was a keyboard interrupt")
            exit("Keyboard Interrupt")
        except:
            print("Something went wrong in fetching the temperature. Trying again... ")
            output = self.getTemp()
            print("This time it worked successfully!")
            return output

    # set the temperature--with recursive error handling
    def setTemp(self, temp: float):
        try:
            if self.isAcceptableTemp(temp):
                server = Telnet("172.24.0.7")
                param = "= SP1 " + str(temp) + "\n"
                server.write(param.encode("ascii"))
                sleep(0.4)
                server.close()
        except KeyboardInterrupt:
            print("There was a keyboard interrupt")
            exit("Keyboard Interrupt")
        except:
            print("There was an error in setting the temperature. Trying again... ")
            self.setTemp(temp)
            print("This time it worked successfully!")