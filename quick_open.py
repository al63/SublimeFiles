import sublime, sublime_plugin
import sys
import os

class QuickOpenCommand(sublime_plugin.WindowCommand):
    def run(self, command):
        if command == "open":
            self.open_new_file()
        elif command == "cd":
            self.change_directory()
        elif command == "setdir":
            self.set_working_directory()

    def change_directory(self):
        self.dir_files = []
        self.dir_files.append("." + " (" + os.getcwd() + ")")
        self.dir_files.append("..")
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(),element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element)
        self.window.show_quick_panel(self.dir_files, self.handle_change_directory,  sublime.MONOSPACE_FONT)

    def handle_change_directory(self, call_value):
        print call_value
        if call_value != -1 and call_value != 0:
            os.chdir(self.dir_files[call_value])
            self.change_directory()

    def open_new_file(self):
        self.dir_files = []
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(), element)
            if not os.path.isdir(fullpath):
                self.dir_files.append(element)
        self.window.show_quick_panel(self.dir_files, self.handle_open_new_file,  sublime.MONOSPACE_FONT)

    def handle_open_new_file(self, call_value):
        if call_value != -1:
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