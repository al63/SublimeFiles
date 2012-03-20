import sublime, sublime_plugin
import os
import glob


class QuickOpen(sublime_plugin.WindowCommand):

    def run(self):
        self.determine_command()


    def determine_command(self):
        self.options = ["edit", "change directory"]
        self.window.show_quick_panel(self.options, self.choose_command, sublime.MONOSPACE_FONT)


    def choose_command(self, call_value):
        self.command = self.options[call_value]
        if self.command == "change directory":
            self.cur_path = os.getenv("HOME")
            self.change_directory()
        else:
            try:
                self.cur_path
            except:
                self.cur_path = os.getenv("HOME")
            self.open_new_file()


    def change_directory(self):
        self.dir_files = []
        for element in os.listdir(self.cur_path):
            fullpath = os.path.join(self.cur_path,element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element)
        self.dir_files.append("REACHED DIR")
        self.window.show_quick_panel(self.dir_files, self.handle_change_directory,  sublime.MONOSPACE_FONT)


    def handle_change_directory(self, call_value):
        if call_value != 1:
            if self.dir_files[call_value] != "REACHED DIR":
                self.cur_path += "/" + self.dir_files[call_value]
                self.change_directory()


    def open_new_file(self):
        self.dir_files = []
        for element in os.listdir(self.cur_path):
            fullpath = os.path.join(self.cur_path, element)
            if not os.path.isdir(fullpath):
                self.dir_files.append(element)
        self.window.show_quick_panel(self.dir_files, self.handle_open_new_file,  sublime.MONOSPACE_FONT)


    def handle_open_new_file(self, call_value):
        print self.dir_files[call_value]
        self.window.open_file(self.cur_path + "/" + self.dir_files[call_value])