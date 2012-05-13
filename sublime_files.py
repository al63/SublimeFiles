import sublime, sublime_plugin
import os, sys, glob
import subprocess

bullet = u'\u2022'
class SublimeFilesCommand(sublime_plugin.WindowCommand):
    global bullet
    def run(self, command):
        try:
            self.home
        except:
            #first time starting up. setup work here.
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
        if command == 'navigate':
            self.open_navigator()


    #function for showing panel for changing directories / opening files
    def open_navigator(self):
        self.dir_files = ['[' + os.getcwd() +']', bullet + ' Directory actions', '..' + os.sep, '~' + os.sep]
        for element in os.listdir(os.getcwd()):
            fullpath = os.path.join(os.getcwd(), element)
            if os.path.isdir(fullpath):
                self.dir_files.append(element + os.sep)
            else:
                self.dir_files.append(element)
        self.dir_files = self.dir_files[:4] + sorted(self.dir_files[4:], key=sort_files)

        if self.bookmark is not None:
            self.dir_files.insert(2, bullet + ' To bookmark (' + self.bookmark + ')')
        if self.window.active_view().file_name() is not None:
            self.dir_files.insert(2, bullet + ' To current view')
            
        self.window.show_quick_panel(self.dir_files, self.handle_navigator_option, sublime.MONOSPACE_FONT)


    #handles user's selection in open_navigator. Either cd's into new directory, or opens file
    def handle_navigator_option(self, call_value):
        if call_value != -1:
            option = self.dir_files[call_value];
            if call_value == 0:
                self.open_navigator()
            elif call_value == 1: #Directory Actions
                self.open_directory_options()
            elif option == '~' + os.sep:
                os.chdir(os.getenv(self.home))
            elif option == '..' + os.sep:
                os.chdir(os.path.pardir)
            elif option == bullet + ' To current view':
                os.chdir(os.path.dirname(self.window.active_view().file_name()))
            elif option.startswith(bullet + ' To bookmark'):
                os.chdir(self.bookmark)
            else: 
                fullpath = os.path.join(os.getcwd(), self.dir_files[call_value])
                if os.path.isdir(fullpath): #navigate to directory
                    os.chdir(self.dir_files[call_value])
                else: #open file
                    self.window.open_file(os.path.join(os.getcwd(), fullpath))
                    return
            self.open_navigator()


    #Options for when a user selects '.'
    def open_directory_options(self): 
        self.directory_options = [bullet+' Add folder to project', bullet+' Create new file', bullet+' Set bookmark here',bullet+' Back']
        #Terminal opening. only for posix at the moment
        if os.name == 'posix' and self.term_command is not None:
            self.directory_options.insert(0, bullet + ' Open terminal here')
        self.window.show_quick_panel(self.directory_options, self.handle_directory_option, sublime.MONOSPACE_FONT)


    #Handle choice for when user selects '.'
    def handle_directory_option(self, call_value):
        if call_value != -1:
            selection = self.directory_options[call_value]
            if selection == bullet + ' Create new file':
                self.window.show_input_panel('File name: ', '', self.handle_new_file, None, None)
            elif selection == bullet + ' Back':
                self.open_navigator()
            elif selection == bullet + ' Set bookmark here':
                self.bookmark = os.getcwd()
                self.open_navigator()
            elif selection == bullet+ ' Open terminal here':
                directory_split = os.getcwd().split()
                actual_dir = ''
                for element in directory_split:
                    actual_dir += element + '\ ' 
                os.system(self.term_command + actual_dir[:len(actual_dir)-2])
            elif selection == bullet + ' Add folder to project':
                sublime_command_line(['-a', os.getcwd()])


    #Handle creating new file
    def handle_new_file(self, file_name):
        if os.path.isfile(os.getcwd() + os.sep + file_name):
            sublime.error_message(file_name + " already exists")
            return

        FILE = open(os.getcwd() + os.sep + file_name, 'a')
        FILE.close()
        self.window.open_file(os.getcwd() + os.sep + file_name)


def sort_files(filename):
    total_weight = 0
    if filename[0] == '.':
        total_weight += 2
    if filename[-1] == '/':
        total_weight += 1
    return total_weight


#Hack to add folders to sidebar (thank you wbond for your forum post!)
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
