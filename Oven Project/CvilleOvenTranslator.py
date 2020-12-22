from time import sleep
from os import system
from OvenTranslator import OvenTranslator
from telnetlib import Telnet


class CvilleOvenTranslator(OvenTranslator):

    def getTemp(self):

        # setup
        server = Telnet("172.24.0.7")
        server.write(b"? C1\n")
        raw_input = server.read_until(b"\r")
        decoded_input = raw_input.decode("ascii")

        # input converter
        float_input = ""
        for char in decoded_input:
            if char.isdigit() or char == ".":
                float_input += char

        server.close()

        return float(float_input)

    def setTemp(self, temp: float):

        if self.isAcceptableTemp(temp):
            server = Telnet("172.24.0.7")
            param = "= SP1 " + str(temp) + "\n"
            server.write(param.encode("ascii"))
            sleep(0.4)
            server.close()