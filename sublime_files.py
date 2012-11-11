import sublime, sublime_plugin
import os, sys, glob
import subprocess
import shlex
import locale
from subprocess import Popen


bullet = u'\u2022'
class SublimeFilesCommand(sublime_plugin.WindowCommand):
    def run(self, command):
        try:
            self.home
        except:
            # first time starting up. ugly, but works
            settings = sublime.load_settings('SublimeFiles.sublime-settings')
            if os.name == 'nt':
                self.home = 'USERPROFILE'
            else:
                self.home = 'HOME'
            try:
                os.chdir(os.path.dirname(sublime.active_window().active_view().file_name()))
            except:
                os.chdir(os.getenv(self.home))
            self.bookmark = None
            self.term_command = settings.get('term_command')
            self.drives = [] # for windows machines

        if command == 'navigate':
            self.open_navigator()

    # function for showing panel for changing directories / opening files
    def open_navigator(self):
        self.dir_files = ['[' + os.getcwdu() + ']', bullet + ' Directory actions', '..' + os.sep, '~' + os.sep]

        # annoying way to deal with windows
        if sublime.platform() == 'windows':
            if len(self.drives) == 0:
                for i in range(ord('A'), ord('Z') + 1):
                    drive = chr(i)
                    if os.path.exists(drive + ":\\"):
                        self.drives.append(drive + ':\\')
            self.dir_files += self.drives

        for element in os.listdir(os.getcwdu()):
            fullpath = os.path.join(os.getcwdu(), element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element + os.sep)
            else:
                self.dir_files.append(element)
        self.dir_files = self.dir_files[:4] + sorted(self.dir_files[4:], key=sort_files)
        if self.bookmark:
            self.dir_files.insert(2, bullet + ' To bookmark (' + self.bookmark + ')')
        if self.window.active_view() and self.window.active_view().file_name():
            self.dir_files.insert(2, bullet + ' To current view')
        self.window.show_quick_panel(self.dir_files, self.handle_navigator_option, sublime.MONOSPACE_FONT)

    # handles user's selection in open_navigator. cd's into new directory, opens cur dir options, or opens file
    def handle_navigator_option(self, call_value):
        if call_value != -1:
            option = self.dir_files[call_value];
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
                fullpath = os.path.join(os.getcwdu(), self.dir_files[call_value])
                if os.path.isdir(fullpath): # navigate to directory
                    os.chdir(self.dir_files[call_value])
                else: # open file
                    self.window.open_file(os.path.join(os.getcwdu(), fullpath))
                    return
            self.open_navigator()

    # options for when a user selects current directory
    def open_directory_options(self): 
        self.directory_options = [bullet + ' Add folder to project', bullet + ' Create new file',
            bullet + ' Create new directory', bullet + ' Set bookmark here', bullet + ' Back']
        # terminal opening. only for osx/linux right now
        if os.name == 'posix' and self.term_command:
            self.directory_options.insert(0, bullet + ' Open terminal here')
        self.window.show_quick_panel(self.directory_options, self.handle_directory_option, sublime.MONOSPACE_FONT)

    # handle choice for when user selects option from currents directory
    def handle_directory_option(self, call_value):
        if call_value != -1:
            selection = self.directory_options[call_value]
            if selection == bullet + ' Create new file':
                self.window.show_input_panel('File name: ', '', self.handle_new_file, None, None)
            elif selection == bullet + ' Back':
                self.open_navigator()
            elif selection == bullet + ' Set bookmark here':
                self.bookmark = os.getcwdu()
                self.open_navigator()
            elif selection == bullet + ' Open terminal here':
                command = shlex.split(str(self.term_command))
                command.append(os.getcwdu())
                try:
                    Popen(command)
                except:
                    sublime.error_message("Unable to open terminal")
            elif selection == bullet + ' Add folder to project':
                sublime_command_line(['-a', os.getcwdu()])
            elif selection == bullet + ' Create new directory':
                self.window.show_input_panel('Directory name: ', '', self.handle_new_directory, None, None)

    def handle_new_file(self, file_name):
        if os.path.isfile(os.getcwdu() + os.sep + file_name):
            sublime.error_message(file_name + " already exists")
            return
        if os.path.isdir(os.getcwdu() + os.sep + file_name):
            sublime.error_message(file_name + " is already a directory")
            return
        FILE = open(os.getcwdu() + os.sep + file_name, 'a')
        FILE.close()
        self.window.open_file(os.getcwdu() + os.sep + file_name)

    def handle_new_directory(self, dir_name):
        if os.path.isfile(os.getcwdu() + os.sep + dir_name):
            sublime.error_message(dir_name + " is already a file")
            return
        if os.path.isdir(os.getcwdu() + os.sep + dir_name):
            sublime.error_message(dir_name + " already exists")
            return
        os.makedirs(os.getcwdu() + os.sep + dir_name)


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
        return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
    elif sublime.platform() == 'linux':
        return open('/proc/self/cmdline').read().split(chr(0))[0]
    else:
        return sys.executable

def sublime_command_line(args):
    args.insert(0, get_sublime_path())
    return subprocess.Popen(args)
