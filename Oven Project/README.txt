Zach Rinehart
01/21/2021
OPUS README

Intro:
	Welcome to my oven project! I named it OPUS (Oven Project Ultimate Service), but you can call it whatever you want. I'm Zach Rinehart, the creator of OPUS, and in this README, I'll be walking you through how it works.
	To introduce you, OPUS is a program that can read and write profiles to the Silicom oven in Charlottesville, VA. The hardware engineers here wanted a way to set temperature profiles for the oven, as a way of adjusting the temprerature over time without having to babysit it. However, this oven is ancient--IBM-type ancient--and so modern software tools were needed to provide a way of implementing this. The way OPUS works is that it uses CSV files (Comma-Separated Value Files) as profiles and reads them to the oven. If you don't know what CSV files are, Google it and educate yourself if you want to use OPUS. OPUS can also do other things, such as loading default settings into the oven that make it more compatible with OPUS, previewing each profile as a graph, and allowing users to play with the theme selector (it makes the program more personal and customizable). 
	OPUS was designed to connect to the oven via the Silicom LAN. In developing OPUS, we came up with the ultimate jerry-rig system. We first used a breakout board to connect a cable to the oven's serial port. The cable then connects to a remote server, which then connects to Ethernet, which computers can connect to over WI-FI. This enables OPUS to be run from anywhere that is connected to the Silicom network, even through a VPN. This configuration also enables users to connect to the oven via Telnet without OPUS to change the oven parameters. To see what language the oven uses, consult the documentation in the oven binder in the Silicom office of Charlottesville.
	Read on for more details of how OPUS works.


Keep in mind:
	A. LOADING DEFAULT SETTINGS TO THE OVEN WILL NOT RESET THE DEGREE UNIT TYPE TO CELSIUS. If the oven happens to be in "Fahrenheit" mode, then it will execute the program in degrees Fahrenheit. OPUS is designed to work in degrees Celsius.
	B. If you launch a debug version of OPUS with a terminal window, you may see a lot of debug messages. That's fine; the program is handling errors correctly.
	C. Below is a list of dependencies for the program:
		1. The program can still communicate with the oven if the oven is not switched "on", but it needs to be switched "on" in order for the profiles to be run.
		2. The remote server (the black box thing to the left side of the oven) must be plugged both into power, the oven, and Ethernet.


Profiles/CSV Files:
	The CSV files for the program are composed of different states. Each row denotes a state. Further, each state is composed of three sections: the Temp section, the Time section, and the Ramp Rate section. The Temp section describes the temperature of the state in degrees Celsius. For example, a Temp value of 50 would mean a value of 50 degrees Celsius for that state. The next section, Time, indicates the time length of that state in minutes. For example, a Time value of 3 would mean that the state goes for 3 minutes. This is also known as the dwell time. The third value, Ramp Rate, describes approximately how fast (in degrees per minute) the oven switches (or “ramps”) to that state. For example, a Ramp Rate of 5 would mean the oven will move approximately 5 degrees per minute to get to that state. Note that due to the limitations of this oven, this value is highly approximate. Note also that the software-encoded temperature limits for the oven are -50 and 90 degrees, and the Ramp Rate limits are 10 for cooling and 17 for heating.

	Put all together, here is an example profile. The first row (state) has a Temp value of 40, a Time value of 3, and a Ramp Rate value of 4. This means that the oven will progress towards 40 degrees Celsius at an approximate rate of 4 degrees per minute. Once it reaches 40 degrees Celsius, it will remain there for 3 minutes before progressing to the next state. Let’s say the next row/state has a Temp value of 30, a Time value of 6, and a Ramp Rate value of 1. This means that the oven will progress from 40 degrees Celsius to 30 degrees Celsius at a rate of 1 degree per minute. Once it hits 30 degrees, it will dwell there for 6 minutes. You will find this example profile in the same folder as this README, so you can view it if you like and even run it if you so desire.
	
	As a further note, there can also be an optional fourth column for comments. As long as the three columns of Time, Temp, and Ramp Rate are present in the CSV file, there can be other columns that do not interfere with the program, including a comments column.

	This program is designed to mimic modern software tools. In a similar fashion to opening a project in a directory (such as in an IDE), the program will let you choose a CSV file from a pop-up file explorer. The best way to utilize this functionality is to organize your profiles under a single master folder (sub-folders permitted). To edit profiles, open them up in a spreadsheet editor (or whatever editor you like) and edit them. The use of spreadsheet editors enables users to create more complex profiles easily and efficiently. To preview the profiles for an estimate of how they will run, run the program, select the desired spreadsheet, and hit the “Display Profile as Graph” button.


Running the Program:

	To run the program, first locate the application (.EXE) file under the "OPUS" folder. Double-click it to launch the application. Most modern programs create a desktop shortcut to this file automatically, but this program does not have an installation process, so shortcuts must be added manually.

	The first selection of options upon launching the program is the Theme Selector. This is not crucial to the operation of the program, but it changes the color theme of the GUI. It was included as a way to make the program more fun and customizable. To change the theme, use the drop-down menu to select one and then click “Update Theme”. To preview the different themes, click the button labeled “Preview Themes”.

	The second selection of options has to do with the profiles/CSV files. The text box details the filepath of the CSV file being used. To change the CSV file, click the “Browse” button. If you would like to save the current CSV file as the default profile for future operations, click the “Save as Default CSV File” button.

	The next buttons have to do with the execution of the profiles. To preview the selected profile to see how it will run, hit the “Display Profile as Graph” button. This will give you a graph estimate of how the profile will run, with time (in minutes) on the x-axis and temperature (in degrees Celsius) on the y-axis. To actually run the program, hit the “Run Profile” button. This will show you both a graph of the estimate of the profile and a graph of the actual temperature of the oven. Both graphs are drawn in the same window (appearing as two lines), but the estimate of the profile will not change, whereas the line depicting the actual temperature of the oven will be drawn throughout the execution of the profile. Note that there are tools on the bottom portion of the window to zoom in or pan around the graph. To pause the profile, hit "Pause Profile". After pausing it, hit "Resume Profile". The "Resume Profile" button has a second purpose, though: if the program crashes, is shut down, or is put on hold for whatever reason, you can always launch the application again and hit "Resume Profile" to resume it from where it was when the program terminated. If you make a mistake and hit "Run Profile" again instead of "Resume Profile", this is not reversible, and you would need to edit the CSV file to adjust the starting point if you'd like it to resume from a different point.
	
	The final two buttons are miscellaneous. The "Load Default Oven Settings" button will load settings into the oven to make it more compatible with OPUS. Use this button if the oven settings have been tweaked and the oven is no longer functional with OPUS (and make sure to write down the settings if you need them before you hit the button). The last button is the "View README" button. Perhaps that's how you got here!
	
	
KNOWN BUGS:
	1. One of the computers tested had issues with Window’s power management functions, specifically with turning off the screen after a period of time. The program would then hang once the time limit was reached. If you experience this behavior, adjust or turn off Window’s power saving features. 
	2. There has sometimes been an issue of getting a false temperature read that stays consistent and then jumps back to the actual read temp. You may notice this as an unintended jump in the graph either positive or negative for a very short time. 
