import sublime, sublime_plugin
import sys

class QuickOpenCommand(sublime_plugin.WindowCommand):
    def run(self, command):
        if command == "navigate":
            self.open_navigator()
        elif command == "setdir":
            self.set_working_directory()

    #function for showing panel for changing directories / opening files
    def open_navigator(self):
        self.dir_files = [". (" + os.getcwd() + ")", ".."]
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(),element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element + "/")
            else:
                self.dir_files.append(element)
        self.dir_files = sorted(self.dir_files, key=sort_files)
        self.window.show_quick_panel(self.dir_files, self.handle_select_option, sublime.MONOSPACE_FONT)

    #handles user's selection in open_navigator. Either cd's into new directory, or opens file
    def handle_select_option(self, call_value):
        if call_value != -1 and call_value != 0:
            fullpath = os.path.join(os.getcwd(),self.dir_files[call_value])
            if os.path.isdir(fullpath):
                os.chdir(self.dir_files[call_value])
                self.open_navigator()
            else:
                self.window.open_file(os.path.join(os.getcwd(), self.dir_files[call_value]))

    #function for changing the current directory 
    def set_working_directory(self):
        self.window.show_input_panel("Set Directory", os.getcwd(), self.handle_set_working_directory, None, None)

    #handles changing the directory based on user input
    def handle_set_working_directory(self, new_dir):
        try:
            if new_dir[0] == "~":
                new_dir = os.getenv("HOME") + new_dir[1:]
                os.chdir(new_dir)
        except:
            sublime.error_message(new_dir + " does not exist")


def sort_files(filename):
    if filename[0:3] == ". (":
        return 0
    if filename == "..":
        return 1
    
    total_weight = 2
    if filename[0] == ".":
        total_weight += 2
    if filename[-1] == "/":
        total_weight += 1
    return total_weight