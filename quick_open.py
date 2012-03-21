import sublime, sublime_plugin
import sys, os

class QuickOpenCommand(sublime_plugin.WindowCommand):
    def run(self, command):
        if command == "navigate":
            self.open_navigator()
        elif command == "setdir":
            self.set_working_directory()

    def open_navigator(self):
        dot_files = []
        dot_directories = []
        directories = []
        files = []
        self.dir_files = []

        self.dir_files.append(". (" + os.getcwd() + ")")
        self.dir_files.append("..")
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(),element)
            if os.path.isdir(fullpath):
                if element[0] == ".":
                    dot_directories.append(element + "/")
                else:
                    directories.append(element+ "/")
            else:
                if element[0] == ".":
                    dot_files.append(element + "/")
                else:
                    files.append(element)

        self.dir_files += files + directories + dot_files + dot_directories
        self.window.show_quick_panel(self.dir_files, self.handle_select_option,  sublime.MONOSPACE_FONT)

    def handle_select_option(self, call_value):
        if call_value != -1 and call_value != 0:
            fullpath = os.path.join(os.getcwd(),self.dir_files[call_value])
            if os.path.isdir(fullpath):
                os.chdir(self.dir_files[call_value])
                self.open_navigator()
            else:
                self.window.open_file(os.path.join(os.getcwd(), self.dir_files[call_value]))

    def set_working_directory(self):
        self.window.show_input_panel("Set directory", "", self.handle_set_working_directory, None, None)

    def handle_set_working_directory(self, new_dir):
        if new_dir[0] == "~":
            new_dir = os.getenv("HOME") + new_dir[1:]
        try:
            os.chdir(new_dir)
        except:
            pass
