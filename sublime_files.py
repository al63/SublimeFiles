import sublime
import sublime_plugin
import os, shutil

class SublimeFilesCommand(sublime_plugin.WindowCommand):
    def run(self, command):
        if command == "navigate":
            self.open_navigator()
        elif command == "setdir":
            self.set_working_directory()

    #function for showing panel for changing directories / opening files
    def open_navigator(self):
        self.dir_files = [". (" + os.getcwd() + ")", ".."]
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(), element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element + "/")
            else:
                self.dir_files.append(element)
        self.dir_files = self.dir_files[:2] + sorted(self.dir_files[2:], key=sort_files)
        self.dir_files.append("~/")
        self.window.show_quick_panel(self.dir_files, self.handle_navigator_option, sublime.MONOSPACE_FONT)

    #handles user's selection in open_navigator. Either cd's into new directory, or opens file
    def handle_navigator_option(self, call_value):
        if call_value != -1 and call_value != 0:
            if self.dir_files[call_value] == "~/":
                os.chdir(os.getenv("HOME"))
                self.open_navigator()
            else:
                fullpath = os.path.join(os.getcwd(), self.dir_files[call_value])
                if os.path.isdir(fullpath):
                    os.chdir(self.dir_files[call_value])
                    self.open_navigator()
                else:
                    self.open_file_options(self.dir_files[call_value])
                    #self.window.open_file(fullpath)

    def open_file_options(self, filename):
        self.current_file = filename 
        self.file_options = ["Open", "Rename", "Move", "Copy", "Delete", "Back"]
        self.window.show_quick_panel(self.file_options, self.handle_file_option, sublime.MONOSPACE_FONT)

    def handle_file_option(self, call_value):
        if call_value != -1:
            selection = self.file_options[call_value]
            if selection == "Back":
                self.open_navigator()
            elif selection == "Open":
                fullpath = os.path.join(os.getcwd(), self.current_file)
                self.window.open_file(fullpath)
            elif selection == "Rename":
                self.window.show_input_panel("Rename File To: ", self.current_file, self.handle_rename_file, None, None)
            elif selection == "Delete":
                os.remove(self.current_file)
            elif selection == "Copy":
                self.is_copy = True
                self.old_path = os.path.join(os.getcwd(), self.current_file)
                self.open_copymove_navigator()
            elif selection == "Move":
                self.is_copy = False
                self.old_path = os.path.join(os.getcwd(), self.current_file)
                self.open_copymove_navigator()

    def open_copymove_navigator(self):
        self.dir_files = [". (" + os.getcwd() + ")", ".."]
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(), element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element + "/")
        self.dir_files = self.dir_files[:2] + sorted(self.dir_files[2:], key=sort_files)
        self.dir_files.append("~/")
        self.window.show_quick_panel(self.dir_files, self.handle_copymove_navigator_option, sublime.MONOSPACE_FONT)

    def handle_copymove_navigator_option(self, call_value):
        if call_value == 0: #if reached directory to copy or move file to
            if self.is_copy == True:
                self.window.show_input_panel("New Name:", self.current_file, self.handle_copy_file, None, None)
            else:
                self.window.show_input_panel("New Name:", self.current_file, self.handle_move_file, None, None)

        elif call_value != -1:
            if self.dir_files[call_value] == "~/":
                os.chdir(os.getenv("HOME"))
            else:
                fullpath = os.path.join(os.getcwd(), self.dir_files[call_value])
                if os.path.isdir(fullpath):
                    os.chdir(self.dir_files[call_value])
            self.open_copymove_navigator()

    def handle_move_file(self, new_name):
        shutil.move(self.old_path, os.path.join(os.getcwd(), new_name))

    def handle_copy_file(self, new_name):
        shutil.copy2(self.old_path, os.path.join(os.getcwd(), new_name))

    def handle_rename_file(self, new_name):
        try:
            os.rename(self.current_file, new_name)
        except:
            sublime.error_message("Unable to rename file")

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
    total_weight = 0
    if filename[0] == ".":
        total_weight += 2
    if filename[-1] == "/":
        total_weight += 1
    return total_weight
