import sublime, sublime_plugin
import os
import glob


class QuickOpenCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.options = ["Edit file", "Change directory", "Set working directory"]
        self.show_commands()

    def show_commands(self):
        self.window.show_quick_panel(self.options, self.choose_command, sublime.MONOSPACE_FONT)


    def choose_command(self, call_value):
        self.command = self.options[call_value]
        if self.command == "Change directory":
            self.change_directory()
        elif self.command == "Edit file":
            self.open_new_file()
        else:
            self.set_working_directory()


    def change_directory(self):
        self.dir_files = []
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(),element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element)
        self.dir_files.append("..")
        self.dir_files.append("Reached directory")
        self.window.show_quick_panel(self.dir_files, self.handle_change_directory,  sublime.MONOSPACE_FONT)


    def handle_change_directory(self, call_value):
        if call_value != 1:
            if self.dir_files[call_value] != "Reached directory":
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
        print new_dir
        try:
            os.chdir(new_dir)
        except:
            pass


