#How to use the BP parse program

# Introduction #
This is a work of progress of mine. It is very poorly documented. Possibly badly coded as well but it works mostly.

I primarily program in a linux/mac/unix environment so this program is configured for such. I think in the code there are hard coded "/" that might need to be changed to work in a windows environment.

Other than that it is all written in standard python version 2.6 not the newer python 3 or whatever it is called.
The program takes two different arguments
a file path
or
-r

The file path should contain only .bp files taken from supcom's units.scd.
There are many unused/civilian units in the supcom units files so you can separate them out using the unitDB.txt file. It contains all the military units of each race in a space/return delimited file.

There is a small subprogram called renamer.py which removes the _unit part of each bp file. This is required for the program to work correctly at this point. It uses the shortened file names as the unit blueprint id._

after the folder with only the military units is created and renamed you can pass its full file path to BPparse. This will take a few minutes as it goes about reading, tokenizing, and parsing every blueprint in the folder passed. Once it has done this it will spit out a rather large python file called output.py. This one very large python object which contains all of the information for all of the units parsed. (warning opening this in a text editor with syntax coloring typically freezes the editor so if you want to look at it open in notepad)

Then the program loads the output.py object and created html pages in a folder called webpages. It will put all of the unit html files in another folder called units\*timestamp

Once you have done this at least once, the output.py object remains and re-parsing all of the units isn't necessary. Primarily I did this so I could rapidly try new ways to output the html files.
This is what -r does.

myDataPrep and unitdetails are primarily the files responsible for spitting out the html. The former is for the index page and the latter is for each unit respectively.

This is still a very work in progress program. It is extremely finicky, not robust, and very single purpose.