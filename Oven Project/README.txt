Zach Rinehart
01/11/2021
Oven Project Manual v2

Intro:
	Welcome to my oven project! I named it OPUS (Oven Project Ultimate Service), but you can call it whatever you want. I'm Zach Rinehart, and in this README, I'll be walking you through how OPUS works.
	To introduce you, OPUS is a program that can read and write profiles to the Silicom oven in Charlottesville, VA. The hardware engineers here wanted a way to set temperature profiles for the oven, as a way of adjusting the temprerature over time without having to babysit it. However, this oven is ancient--IBM-type ancient--and so modern software tools were needed to provide a way of implementing this. The way OPUS works is that it uses CSV files (Comma-Seperated Value Files) as profiles and reads them to the oven. If you don't know what CSV files are, Google it and educate yourself if you want to use OPUS. OPUS can also do other things, such as loading default settings into the oven that make it more compatible with OPUS, previewing each profile as a graph, and allowing users to play with the theme selector (it makes the program more personal and customizable). 
	OPUS was designed to connect to the oven via the LAN. In developing OPUS, we came up with the ultimate jerry-rig system. We first used a breakout board to connect a cable to the oven's serial port. The cable then connects to a remote server, which then connects to Ethernet, which computers can connect to over WI-FI. This enables OPUS to be run from anywhere that is connected to the ADI WI-FI network, even through a VPN. This configuration also enables users to connect to the oven via Telnet without OPUS to change the oven parameters wirelessly. To see what language the ove uses, consult the documentation in the oven binder in the Silicom office of Charlottesville.
	Read on for more details of how OPUS works.

Setup and Inner Workings:
	Below is a list of dependancies for the program:
	1. The program can still communicate with the oven if the oven is not switched "on", but it needs to be switched "on" in order for the profiles to be run.
	2. The remote server (the black box thing to the left side of the oven) must be plugged both into power, the oven, and Ethernet.

Profiles/CSV Files:
	The CSV files for the program are composed of different states. Each row denotes a state. Further, each state is composed of three sections: the Temp section, the Time section, and the Ramp Rate section, in this order. The Temp section describes the temperature of the state in degrees Celsius. For example, a Temp value of 50 would mean a value of 50 degrees Celsius for that state. The next section, Time, indicates the time length of that state in minutes. For example, a Time value of 3 would mean that the state goes for 3 minutes. This is also known as the dwell time. The third value, Ramp Rate, describes approximately how fast (in degrees per minute) the oven switches (or “ramps”) to that state. For example, a Ramp Rate of 5 would mean the oven will move approximately 5 degrees per minute to get to that state. Note that due to the complications of a dated oven, this value is highly approximate.

	Put all together, here is an example profile. The first row (state) has a Temp value of 40, a Time value of 3, and a Ramp Rate value of 4. This means that the oven will progress towards 40 degrees Celsius at an approximate rate of 4 degrees per minute. Once it reaches 40 degrees Celsius, it will remain there for 3 minutes before progressing to the next state. Let’s say the next row/state has a Temp value of 30, a Time value of 6, and a Ramp Rate value of 1. This means that the oven will progress from 40 degrees Celsius to 30 degrees Celsius at a rate of 1 degree per minute. Once it hits 30 degrees, it will dwell there for 6 minutes.

	This program is designed to mimic modern software tools. In a similar fashion to opening a project in a directory (such as in an IDE), the program will let you choose a CSV file from a pop-up file explorer. The best way to utilize this functionality is to organize your profiles under a single master folder (sub-folders permitted). To edit profiles, open them up in a spreadsheet editor and edit them. The use of spreadsheet editors enables users to create more complex profiles easily and efficiently. To preview the profiles for an estimate of how they will run, run the program, select the desired spreadsheet, and hit the “Display Profile as Graph” button.


Running the Program:

	To run the program, first locate the application (.EXE) file under the “OvenProjectZ” folder. Double-click it to launch the application. Most modern programs create a desktop shortcut to this file, but this program does not have an installation process, so shortcuts must be added manually.

	The first selection of options upon launching the program is the Theme Selector. This is not crucial to the operation of the program, but it changes the color theme of the GUI. It was included as a way to make the program more fun and customizable. To change the theme, use the drop-down menu to select one and then click “Update Theme”. To preview the different themes, click the button labeled “Preview Themes”.

	The second selection of options has to do with the profiles/CSV files. The text box details the filepath of the CSV file being used. To change the CSV file, click the “Browse” button. If you would like to save the current CSV file as the default profile for future operations, click the “Save as Default CSV File” button.

	The final two buttons have to do with the execution of the profiles. To preview the selected profile to see how it will run, hit the “Display Profile as Graph” button. This will give you a graph estimate of how the profile will run, with time (in minutes) on the x-axis and temperature (in degrees Celsius) on the y-axis. To actually run the program, hit the “Run Profile” button. This will show you both a graph of the estimate of the profile and a graph of the actual temperature of the oven. Both graphs are drawn in the same window (appearing as two lines), but the estimate of the profile will not change, whereas the line depicting the actual temperature of the oven will be drawn throughout the execution of the profile.
	
KNOWN BUGS:
	1. OPUS currently runs on my computer, but it will not run on the second-tested computer (Len's) without eventually hanging or becoming unresponsive. Both the Python file and two versions of the EXE file (built with different tools) seem to run fine on my computer, but Len's computer does not seem to like either EXE file. Len does not have Python on his computer, so the Python file has not been tested on his computer. We are currently debugging this issue.
	
