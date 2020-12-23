from time import sleep
from os import system
from OvenTranslator import OvenTranslator
from telnetlib import Telnet


class CvilleOvenTranslator(OvenTranslator):

    def load_default_settings(self):
        # setup
        server = Telnet("172.24.0.7")
        server.write(b"= PB1 5.5")
        server.write(b"= PB2 1.5")
        server.write(b"= RE1 0.00")
        server.write(b"= RE2 0.00")
        server.write(b"= RA1 0.00")
        server.write(b"= RA2 0.35")
        server.write(b"= CT1 5")
        server.write(b"= CT2 5")
        server.write(b"= DB 0.0")
        server.write(b"= CAL 0.0")
        server.write(b"= AUT 0")
        server.write(b"= C_F C")
        server.write(b"= RL -73.4")
        server.write(b"= RH 200.0")

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