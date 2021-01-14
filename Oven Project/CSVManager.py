import csv
from os import path


class CSVManager:

    def __init__(self):
        self.csv_config = open("Config.csv", "w+")
        self.csv_profiles_dir = open("Profiles_Dir.csv", "w+")

        self.csv_profiles_writer = csv.writer(self.csv_profiles_dir)

        self.profilesDict = csv.DictReader(self.csv_profiles_dir)

    # add a new profile
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

    # modify a profile
    def modProfile(self, profileName: str, dictList: [{}]):

        if path.exists(profileName):
            profile = open(profileName, "w")
            writer = csv.DictWriter(profile, fieldnames=["Time", "Temp"])

            writer.writeheader()
            writer.writerows(dictList)

            profile.close()
            return

        print("Error: This file does not exist, cannot write to it")

    # read a profile
    # returns a list of dictionaries
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
            elem["Temp"] = round(float(elem["Temp"]), 1)
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

    # check if a profile is in a valid format
    # returns true if all correct and a string with error message if something is incorrect
    def verifyFormat(self, fileName: str):
        if fileName.endswith(".csv"):
            profile = open(fileName, "r")               # open the file
            profileReader = csv.DictReader(profile)     # create reader from opened file
            fields = profileReader.fieldnames           # get list of fieldnames
            dictList = []  # create empty list of csv elements

            # check all fieldnames
            if "Time" in fields and "Temp" in fields and "Ramp Rate" in fields:

                # add csv items to list from reader
                for row in profileReader:
                    dictList.append(row)

                # check the elements in CSV file
                for elem in dictList:
                    if not (elem["Time"] != None and elem["Time"].replace('.', '', 1).isdigit()
                            and elem["Temp"] != None and elem["Temp"].replace('-', '', 1).replace('.', '', 1).isdigit()
                            and elem["Ramp Rate"] != None and elem["Ramp Rate"].replace('.', '', 1).isdigit()):

                        return "Error: Incorrect element in CSV file"

                # return true if all elements checked and correct
                return True

            # return error if not all correct fields
            return "Error: Missing correct field names"

        # return error if not a csv file
        return "Error: Not a CSV file"