import csv
from os import path


class OwenCSVManager:

    def __init__(self):
        self.csv_config = open("Config.csv", "w+")
        self.csv_profiles_dir = open("Profiles_Dir.csv", "w+")

        self.csv_profiles_writer = csv.writer(self.csv_profiles_dir)

        self.profilesDict = csv.DictReader(self.csv_profiles_dir)

    def addProfile(self, name: str):
        fileName = name

        # if the file already exist:
        if path.exists(fileName):

            # give cautionary message
            decision = input("This file already exists! Overwrite and continue? (y/n) ")
            decision = decision.lower()

            # loop until valid input is given
            while decision != "y" and decision != "n":
                decision = input("Try again: ")
                decision = decision.lower()

            # return false if not overwrite and continue
            if decision == "n":
                return False

        # create the file
        with open(fileName, "w+") as newFile:

            # setup  the fieldnames
            fieldnames = ["Temp", "Time", "Ramp Rate", "Comments"]
            fieldWriter = csv.DictWriter(newFile, fieldnames=fieldnames)
            fieldWriter.writeheader()

            # close the file
            newFile.close()

        return True

    def modProfile(self, profileName: str, dictList: [{}]):

        if path.exists(profileName):
            profile = open(profileName, "w")
            writer = csv.DictWriter(profile, fieldnames=["Time", "Temp"])

            writer.writeheader()
            writer.writerows(dictList)

            profile.close()
            return

        print("Error: This file does not exist, cannot write to it")

    def readProfile(self, fileName: str):

        # setup
        profile = open(fileName, "r")               # open the file
        profileReader = csv.DictReader(profile)     # create reader from opened file
        dictList = []                               # create empty list of csv elements

        # add csv items to list from reader
        for row in profileReader:
            dictList.append(row)

        # convert elements to float
        for elem in dictList:
            elem["Time"] = float(elem["Time"])
            elem["Temp"] = float(elem["Temp"])
            elem["Ramp Rate"] = float(elem["Ramp Rate"])

        # close file
        profile.close()

        # return the list
        return dictList

    # extract list of just x values
    def xtract(self, dictList: [{}]):

        # empty list for x values
        xlist = []

        # store x values
        for elem in dictList:
            xlist.append(elem["Time"])

        return xlist

    # extract list of just y values
    def ytract(self, dictList: [{}]):

        # empty list for y values
        ylist = []

        # store x values
        for elem in dictList:
            ylist.append(elem["Temp"])

        return ylist

    # extract list of just y values
    def ztract(self, dictList: [{}]):

        # empty list for z values
        zlist = []

        # store x values
        for elem in dictList:
            zlist.append(elem["Ramp Rate"])

        return zlist