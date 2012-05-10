Sublime Files
=============

__A keyboard driven file navigation/opening plugin for Sublime Text 2__

------------

Sublime Files works entirely through the command palette. By running the
Sublime Files Navigator, you can "cd" around directories similar to how
you would on a command line in order to open up files. New files will open up in new tabs.


Because Sublime Files actually navigates the file system by changing directories,
the navigator remembers and starts from last visited directory on subsequent uses.
To open the navigator, you can either just invoke the command pallette command or
use the keybinding ctrl+super+n 


Built with Mac OSX, but all the calls have been designed to be platform agnostic and thus should work
regardless of system. However, this is untested on Windows.

----------

__Installation__

Sublime Files can be installed through Sublime Package Control

----------

__Usage__

Sublime files an be activated with the command palette command: "Sublime Files: Open Navigator", or with
the key command ctrl+super+n (or ctrl+alt+n for windows).

Directories and files will show up. By selecting a directory, Sublime Files will move into the directory.
By selecting a file, Sublime Files will pop up options that can be applied onto the file.

Options of note are ".", "..", "~/", and "\* To current view". 

"." Stays in the current directory, and provides potential options for manipulating the current directory. 
(current only allows creating new files into the directory).

".." navigates one level above the current directory, "~/" goes to the home directory, and "\* To current view" goes to the directory containing the current file being edited.
