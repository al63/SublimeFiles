Sublime Files
=============

A keyboard driven file navigation/opening plugin for Sublime Text 2/3.

![Plugin in action](http://i.imgur.com/grlinzi.gif)

Sublime Files works entirely through the command palette. By running the Sublime Files Navigator, you can "`cd`" around directories similar to how you would on a command line in order to open up files. New files will open up in new tabs.

Because Sublime Files actually navigates the file system by changing directories, the navigator remembers and starts from last visited directory on subsequent uses. To open the navigator, you can either just invoke the *Command Palette...* command or use the keybinding:
-  OSX: `ctrl + cmd + n` 
-  Windows/Linux: `ctrl + alt + n`

Installation
------------

Sublime Files can be installed through Sublime Package Control.

Usage
-----

Sublime files an be activated with the *Command Palette...* command: *Sublime Files: Open Navigator*, or with the key command `ctrl + cmd + n` (or `ctrl + alt + n` for Windows / Linux). The first option will always show the current directory. Selecting another directory will navigate to that directory and selecting a file will open that file.

There are a few notable options:

- Selecting *Directory actions* will pop up a small list of actions that can be applied onto the current directory. Mainly, a user can create new files, add the directory to the current project, and open a terminal at the directory.
- Selecting *~/* navigates to the home directory.
- Selecting *../* navigates to the parent directory.
- Selecting *To current view* navigates to the directory of the current file being edited.

Configuration 
-------------

__Ignore file types__

SublimeFiles by default will ignore `*.pyc` files and `*.class` files. You can modify the list of ignored files by changing the `ignore_list` in `SublimeFiles.sublime-settings` (Preferences->Package Settings->Sublime Files->Settings - Default). For example:

	{
	    "ignore_list": ["*.pyc", "*.class", "*.o"]
	}

__Open Terminal__

For OS X/Linux systems, Sublime Files can open up a terminal at the current directory navigated to. In order for this feature to work properly, you will have to modify the `term_command` field in the `SublimeFiles.sublime-settings` file (Preferences->Package Settings->Sublime Files->Settings - Default). As a default, it is set to open up Terminal.app for OS X systems. 

For example, Gnome Terminal and iTerm2 users respectively will want to change term\_command in `SublimeFiles.sublime-settings` to: 

	{
	    "term_command": "gnome-terminal --working-directory="
	}

and

	{
	    "term_command" : "open -a iTerm\ 2 "
	}
