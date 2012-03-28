Sublime Files
=============

__A keyboard driven file management/navigation/opening plugin for Sublime Text 2__

------------

Sublime Files works entirely through the command palette. By running the
Sublime Files Navigator, you can "cd" around directories similar to how
you would on a command line. On selecting a file, a user is presented with 
the following options:


* Open
* Rename
* Delete
* Copy
* Move


Because Sublime Files actually navigates the file system by changing directories,
the navigator remembers and starts from last visited directory on subsequent uses.
To open the navigator, you can either just invoke the command pallette command or
use the keybinding ctrl+super+n 


Built with Mac OSX, but all the calls have been designed to be platform agnostic and thus should work
regardless of system. However, this is untested on Windows.