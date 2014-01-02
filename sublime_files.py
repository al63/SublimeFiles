import os
import sys
import glob
import shlex
import sublime
import sublime_plugin
from fnmatch import fnmatch
from subprocess import Popen

bullet = u'\u2022'


class SublimeFilesCommand(sublime_plugin.WindowCommand):

    def getcwd(self):
        if running_in_st3():
            return os.getcwd()
        else:
            return os.getcwdu()

    def show_quick_panel(self, elements, on_selection, params):
        sublime.set_timeout(lambda: self.window.show_quick_panel(elements, on_selection, params), 10)

    def run(self, command):
        try:
            self.home
        except:
            self.current_dir = ""
            # first time starting up. ugly, but wosrks
            settings = sublime.load_settings('SublimeFiles.sublime-settings')
            if os.name == 'nt':
                self.home = 'USERPROFILE'
            else:
                self.home = 'HOME'
            self.project_root = None
            self.bookmark = None
            self.term_command = settings.get('term_command')
            self.ignore_list = settings.get('ignore_list')
            self.start_directory = settings.get('start_directory')
            if self.start_directory is not None:
                self.start_directory = os.path.abspath(os.path.expanduser(self.start_directory))
                if not os.path.exists(self.start_directory):
                    print ('SublimeFiles: "start_directory" points to invalid path, ignoring.')
                    self.start_directory = None
            self.drives = []  # for windows machines

        if command == 'navigate':
            if self.start_directory is not None:
                os.chdir(self.start_directory)

            self.open_navigator()

    # function for showing panel for changing directories / opening files
    def open_navigator(self):
        if self.start_directory is None:
            self.check_project_root()
        self.current_dir = self.getcwd()
        self.dir_files = ['[' + self.getcwd() + ']',
            bullet + ' Directory actions', '..' + os.sep, '~' + os.sep]

        # annoying way to deal with windows
        if sublime.platform() == 'windows':
            if len(self.drives) == 0:
                for i in range(ord('A'), ord('Z') + 1):
                    drive = chr(i)
                    if (os.path.exists(drive + ':\\')):
                        self.drives.append(drive + ':\\')
            self.dir_files += self.drives

        for element in os.listdir(self.getcwd()):
            ignore_element = False
            for ignore_pattern in self.ignore_list:
                if fnmatch(element, ignore_pattern):
                    ignore_element = True
                    break
            if not ignore_element:
                fullpath = os.path.join(self.getcwd(), element)
                if os.path.isdir(fullpath):
                    self.dir_files.append(element + os.sep)
                else:
                    self.dir_files.append(element)

        self.dir_files = self.dir_files[:4] + sorted(self.dir_files[4:], key=sort_files)

        if self.bookmark:
            self.dir_files.insert(2, bullet + ' To bookmark (' + self.bookmark + ')')
        if self.window.active_view() and self.window.active_view().file_name():
            self.dir_files.insert(2, bullet + ' To current view')

        self.show_quick_panel(self.dir_files, self.handle_navigator_option, sublime.MONOSPACE_FONT)

    # checks if the user has opened up a folder, and if so automatically navigate to the root
    def check_project_root(self):
        folders = self.window.folders()
        if len(folders) > 0:
            # If not one yet present or if has changed
            if not self.project_root or self.project_root != folders[0]:
                self.project_root = folders[0]
                os.chdir(self.project_root)
        elif self.project_root:
            # if folders is empty now and we had a root, let's clear it out
            self.project_root = None

    # handles user's selection from open_navigator
    def handle_navigator_option(self, call_value):
        os.chdir(self.current_dir)
        if call_value != -1:
            option = self.dir_files[call_value]
            if call_value == 0:
                self.open_navigator()
            elif call_value == 1:
                self.open_directory_options()
            elif option == '~' + os.sep:
                os.chdir(os.getenv(self.home))
            elif option == '..' + os.sep:
                os.chdir(os.path.pardir)
            elif sublime.platform() == 'windows' and option in self.drives:
                os.chdir(option)
            elif option == bullet + ' To current view':
                os.chdir(os.path.dirname(self.window.active_view().file_name()))
            elif option.startswith(bullet + ' To bookmark'):
                os.chdir(self.bookmark)
            else:
                fullpath = os.path.join(self.getcwd(), self.dir_files[call_value])
                if os.path.isdir(fullpath):  # navigate to directory
                    os.chdir(self.dir_files[call_value])
                else:  # open file
                    self.window.open_file(os.path.join(self.getcwd(), fullpath))
                    return
            self.open_navigator()

    # options for when a user selects current directory
    def open_directory_options(self):
        self.directory_options = [bullet + ' Add folder to project', bullet + ' Create new file',
            bullet + ' Create new directory', bullet + ' Set bookmark here', bullet + ' Navigate to specific directory', bullet + ' Back']
        # terminal opening. only for osx/linux right now
        if os.name == 'posix' and self.term_command:
            self.directory_options.insert(0, bullet + ' Open terminal here')
        self.show_quick_panel(self.directory_options, self.handle_directory_option, sublime.MONOSPACE_FONT)

    # handle choice for when user selects option from current directory
    def handle_directory_option(self, call_value):
        if call_value != -1:
            selection = self.directory_options[call_value]
            if selection == bullet + ' Create new file':
                self.window.show_input_panel('File name: ', '', self.handle_new_file, None, None)
            elif selection == bullet + ' Back':
                self.open_navigator()
            elif selection == bullet + ' Set bookmark here':
                self.bookmark = self.getcwd()
                self.open_navigator()
            elif selection == bullet + ' Open terminal here':
                command = shlex.split(str(self.term_command))
                command.append(self.getcwd())
                try:
                    Popen(command)
                except:
                    sublime.error_message('Unable to open terminal')
            elif selection == bullet + ' Add folder to project':
                sublime_command_line(['-a', self.getcwd()])
            elif selection == bullet + ' Create new directory':
                self.window.show_input_panel('Directory name: ', '', self.handle_new_directory, None, None)
            elif selection == bullet + ' Navigate to specific directory':
                self.window.show_input_panel("Navigate to: ", self.getcwd(), self.handle_cwd, None, None)

    def handle_new_file(self, file_name):
        if os.path.isfile(self.getcwd() + os.sep + file_name):
            sublime.error_message(file_name + ' already exists')
            return
        if os.path.isdir(self.getcwd() + os.sep + file_name):
            sublime.error_message(file_name + ' is already a directory')
            return
        FILE = open(self.getcwd() + os.sep + file_name, 'a')
        FILE.close()
        self.window.open_file(self.getcwd() + os.sep + file_name)

    def handle_new_directory(self, dir_name):
        if os.path.isfile(self.getcwd() + os.sep + dir_name):
            sublime.error_message(dir_name + ' is already a file')
            return
        if os.path.isdir(self.getcwd() + os.sep + dir_name):
            sublime.error_message(dir_name + ' already exists')
            return
        os.makedirs(self.getcwd() + os.sep + dir_name)

    def handle_cwd(self, new_dir):
        try:
            if new_dir[0] == "~":
                new_dir = os.getenv(self.home) + new_dir[1:]
            os.chdir(new_dir)
        except:
            sublime.error_message(new_dir + " does not exist")


def running_in_st3():
    return int(sublime.version()) >= 3000


def sort_files(filename):
    total_weight = 0
    if filename[0] == '.':
        total_weight += 2
    if filename[-1] == os.sep:
        total_weight += 1
    return total_weight


# hack to add folders to sidebar (stolen from wbond)
def get_sublime_path():
    if sublime.platform() == 'osx':
        if running_in_st3():
            return '/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl'
        else:
            return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
    elif sublime.platform() == 'linux':
        return open('/proc/self/cmdline').read().split(chr(0))[0]
    else:
        if running_in_st3():
            return os.path.join(sys.path[0], 'sublime_text.exe')
        else:
            return sys.executable


def sublime_command_line(args):
    args.insert(0, get_sublime_path())
    return Popen(args)
