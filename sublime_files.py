import sublime, sublime_plugin
import os, sys
from subprocess import call

class SublimeFilesCommand(sublime_plugin.WindowCommand):
    def run(self, command):
        try:
            self.home
        except:
            #first time starting up. setup home and change to appropriate start directory
            if os.name == "nt":
                self.home = "USERPROFILE"
            else:
                self.home = "HOME"
            try:
                os.chdir(os.path.dirname(sublime.active_window().active_view().file_name()))
            except:
                os.chdir(os.getenv(self.home))
            self.bookmark = None

        #handle command
        if command == "navigate":
            self.open_navigator()


    #function for showing panel for changing directories / opening files
    def open_navigator(self):
        self.dir_files = ["." + "(" + os.getcwd() +")", "..", "~/"]
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(), element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element + "/")
            else:
                self.dir_files.append(element)
        self.dir_files = self.dir_files[:3] + sorted(self.dir_files[3:], key=sort_files)

        if self.window.active_view().file_name() is not None:
            self.dir_files.append("* To current view")
        if self.bookmark is not None:
            self.dir_files.append("* To bookmark (" + self.bookmark + ")")
            
        self.window.show_quick_panel(self.dir_files, self.handle_navigator_option, sublime.MONOSPACE_FONT)


    #handles user's selection in open_navigator. Either cd's into new directory, or opens file
    def handle_navigator_option(self, call_value):
        if call_value != -1:
            option = self.dir_files[call_value];
            if call_value == 0: #handle directory actions
                self.open_directory_options()
            elif option == "~/":
                os.chdir(os.getenv(self.home))
            elif option == "..":
                os.chdir(os.path.pardir)
            elif option == "* To current view":
                os.chdir(os.path.dirname(self.window.active_view().file_name()))
            elif option.startswith("* To bookmark"):
                os.chdir(self.bookmark)
            else:
                fullpath = os.path.join(os.getcwd(), self.dir_files[call_value])
                if os.path.isdir(fullpath):
                    os.chdir(self.dir_files[call_value])
                else:
                    self.window.open_file(os.path.join(os.getcwd(), fullpath))
                    return
            self.open_navigator()


    #Options for when a user selects "."
    def open_directory_options(self): 
        if self.home == "HOME":
            self.directory_options = ["* Create new file", "* Set bookmark here","* Back"]
            #Terminal opening really mac only as of now...
            if sys.platform == "darwin":
                self.directory_options.append("* Open terminal here")
            self.window.show_quick_panel(self.directory_options, self.handle_directory_option, sublime.MONOSPACE_FONT)


    #Handle choice for when user selects "."
    def handle_directory_option(self, call_value):
        if call_value != -1:
            selection = self.directory_options[call_value]
            if selection == "* Create new file":
                self.window.show_input_panel("File name: ", "", self.handle_new_file_name, None, None)
            elif selection == "* Back":
                self.open_navigator()
            elif selection == "* Set bookmark here":
                self.bookmark = os.getcwd()
                self.open_navigator()
            elif selection == "* Open terminal here":
                directory_split = os.getcwd().split()
                actual_dir = ""
                for element in directory_split:
                    actual_dir += element + "\ " 
                os.system("open -a Terminal " + actual_dir[:len(actual_dir)-2])


    def handle_new_file_name(self, file_name):
        call(["touch", file_name])
        self.window.open_file(file_name)


def sort_files(filename):
    total_weight = 0
    if filename[0] == ".":
        total_weight += 2
    if filename[-1] == "/":
        total_weight += 1
    return total_weight
