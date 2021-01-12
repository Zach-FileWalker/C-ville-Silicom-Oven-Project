from time import sleep
from os import system
from OvenTranslator import OvenTranslator
from telnetlib import Telnet
from time import sleep
from sys import exit


class CvilleOvenTranslator(OvenTranslator):

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

    def is_float(self, value):
        try:
            float(value)
            return True
        except:
            return False

    # #######################################
    #
    #     decoded_input = ""
    #
    #     # while decoded_input is not a decimal
    #     while not self.is_float(decoded_input):
    #
    #         # setup
    #         server = Telnet("172.24.0.7")
    #         server.write(b"? C1\n")
    #         raw_input = server.read_until(b"\r")
    #         decoded_input = raw_input.decode("ascii")
    #
    #         # input converter
    #         for char in decoded_input:
    #             if char.isdigit() or char == "." or char == "-":
    #                 decoded_input += char
    #
    #         server.close()
    #
    #     return float(decoded_input)
    
    def getTemp_sub(self):
        finalval = 0
        inputs = []
        # flag = 0        # DEBUG

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

                # print(self.is_float(float_input))

                # DEBUG
                if len(float_input) > 4 or not self.is_float(float_input):
                    print("DEBUG: NONRETURN " + str(float_input))
                #     flag = 1

                # print(float_input)

                server.close()

            inputs.append(float(float_input))

        # DEBUG
        # if flag == 1:
        #     print("Breakpoint")
        #     flag = 0
        #     print(finalval)
        #     flag = 0

        if abs(inputs[0] - inputs[1]) < 1:
            finalval = inputs[0]
        else:
            print("DEBUG: Recursive Breakpoint")
            print("DEBUG: Former: " + str(inputs[0]) + " and " + str(inputs[1]))
            finalval = self.getTemp()
            print("DEBUG: Finalval: " + str(finalval))

        # DEBUG
        # print(finalval)

        return finalval

        # return float(float_input)

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