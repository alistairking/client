#
# demo to start os command
#
# from subprocess import check_output

# cmd = r'C:\cygwin64\bin\ps.exe'
# output = check_output(cmd)
# print (output)

from __future__ import print_function
import subprocess
import glob
import json
import platform
import os
from cloudmesh_client.util import path_expand


class Shell(object):
    cygwin_path = 'bin'  # i copied fom C:\cygwin\bin

    command = {
        'windows': {},
        'linux': {},
        'darwin': {}
    }

    '''

    big question for badi and others

    how do we now define dynamically functions based on a list that we want to support

    what we want is where args are multiple unlimited parameters to the function

    def f(args...):
        name = get the name from f
        a = list of args...

        cls.execute(cmd, arguments=a, capture=True, verbose=False)

    commands = ['ps', 'ls', ..... ]
    for c in commands:
        generate this command and add to this class dynamically

    or do something more simple

    ls = cls.execute('cmd', args...)   # i think that is what badi does

    '''

    @classmethod
    def ls(cls, *args):
        return cls.execute('ls', args)

    @classmethod
    def ps(cls, *args):
        return cls.execute('ps', args)

    @classmethod
    def bash(cls, *args):
        return cls.execute('bash', args)

    @classmethod
    def cat(cls, *args):
        return cls.execute('cat', args)

    @classmethod
    def git(cls, *args):
        return cls.execute('git', args)

    @classmethod
    def VBoxManage(cls, *args):
        return cls.execute('VBoxManage', args)

    @classmethod
    def blockdiag(cls, *args):
        return cls.execute('blockdiag', args)

    @classmethod
    def cm(cls, *args):
        return cls.execute('cm', args)

    @classmethod
    def fgmetric(cls, *args):
        return cls.execute('fgmetric', args)

    @classmethod
    def fgrep(cls, *args):
        return cls.execute('fgrep', args)

    @classmethod
    def gchproject(cls, *args):
        return cls.execute('gchproject', args)

    @classmethod
    def gchuser(cls, *args):
        return cls.execute('gchuser', args)

    @classmethod
    def glusers(cls, *args):
        return cls.execute('glusers', args)

    @classmethod
    def gmkproject(cls, *args):
        return cls.execute('gmkproject', args)

    @classmethod
    def grep(cls, *args):
        return cls.execute('grep', args)

    @classmethod
    def gstatement(cls, *args):
        return cls.execute('gstatement', args)

    @classmethod
    def head(cls, *args):
        return cls.execute('head', args)

    @classmethod
    def keystone(cls, *args):
        return cls.execute('keystone', args)

    @classmethod
    def kill(cls, *args):
        return cls.execute('kill', args)

    @classmethod
    def ls(cls, *args):
        return cls.execute('ls', args)

    @classmethod
    def mongoimport(cls, *args):
        return cls.execute('mongoimport', args)

    @classmethod
    def mysql(cls, *args):
        return cls.execute('mysql', args)

    @classmethod
    def nosetests(cls, *args):
        return cls.execute('nosetests', args)

    @classmethod
    def nova(cls, *args):
        return cls.execute('nova', args)

    @classmethod
    def ping(cls, *args):
        return cls.execute('ping', args)

    @classmethod
    def pwd(cls, *args):
        return cls.execute('pwd', args)

    @classmethod
    def rackdiag(cls, *args):
        return cls.execute('rackdiag', args)

    @classmethod
    def rm(cls, *args):
        return cls.execute('rm', args)

    @classmethod
    def rsync(cls, *args):
        return cls.execute('rsync', args)

    @classmethod
    def scp(cls, *args):
        return cls.execute('scp', args)

    @classmethod
    def sort(cls, *args):
        return cls.execute('sort', args)

    @classmethod
    def sh(cls, *args):
        return cls.execute('sh', args)

    @classmethod
    def ssh(cls, *args):
        return cls.execute('ssh', args)

    @classmethod
    def sudo(cls, *args):
        return cls.execute('sudo', args)

    @classmethod
    def tail(cls, *args):
        return cls.execute('tail', args)

    @classmethod
    def vagrant(cls, *args):
        return cls.execute('vagrant', args)

    @classmethod
    def mongod(cls, *args):
        return cls.execute('mongod', args)

    @classmethod
    def grep(cls, *args):
        return cls.execute('grep', args)

    @classmethod
    def dialog(cls, *args):
        return cls.execute('dialog', args)

    @classmethod
    def pip(cls, *args):
        return cls.execute('pip', args)

    @classmethod
    def remove_line_with(cls, lines, what):
        result = []
        for line in lines:
            if what not in line:
                result = result + [line]
        return result

    @classmethod
    def find_lines_with(cls, lines, what):
        result = []
        for line in lines:
            if what in line:
                result = result + [line]
        return result

    def __init__(cls):
        if cls.operating_system() == "windows":
            cls.find_cygwin_executables()
        else:
            pass
            # implement for cmd, for linux we can just pass as it includes everything

    @classmethod
    def find_cygwin_executables(cls):
        """
        find the executables 
        """
        exe_paths = glob.glob(cls.cygwin_path + r'\*.exe')
        # print cls.cygwin_path
        # list all *.exe in  cygwin path, use glob
        for c in exe_paths:
            exe = c.split('\\')
            name = exe[1].split('.')[0]
            # command['windows'][name] = "{:}\{:}.exe".format(cygwin_path, c)
            cls.command['windows'][name] = c

    @classmethod
    def terminal_type(cls):
        """
        returns  darwin, cygwin, cmd, or linux
        """
        what = platform.system().lower()

        kind = 'UNDEFINED_TERMINAL_TYPE'
        if 'linux' in what:
            kind = 'linux'
        elif 'darwin' in what:
            kind = 'darwin'
        elif 'cygwin' in what:
            kind = 'cygwin'
        elif 'windows' in what:
            kind = 'windows'

        return kind

    @classmethod
    def which(cls, command):
        t = cls.ttype()
        if 'windows' in t and cls.command_exists(name):
            return cls.command['windows'][name]
        elif 'linux' in t:
            cmd = ["which", command]
            result = subprocess.check_output(cmd).rstrip()
            if len(result) == 0:
                return None
            else:
                return result

    @classmethod
    def command_exists(cls, name):
        t = cls.ttype()
        if 'windows' in t:
            # only for windows
            cls.find_cygwin_executables()
            return name in cls.command['windows']
        elif 'linux' in t:
            r = which(name)
            return r

    @classmethod
    def list_commands(cls):
        t = cls.ttype()
        if 'windows' in t:
            # only for windows
            cls.find_cygwin_executables()
            print ('\n'.join(cls.command['windows']))
        else:
            print ("ERROR: this command is not supported for this OS")

    @classmethod
    def operating_system(cls):
        return platform.system().lower()

    @classmethod
    def execute(cls, cmd, arguments=""):
        """Run Shell command

        :param cmd: command to run
        :param arguments: we dont know yet
        :param capture: if true returns the output
        :return:
        """
        # print "--------------"
        terminal = cls.terminal_type()
        # print cls.command
        os_command = [cmd]
        if terminal in ['linux', 'windows']:
            os_command = [cmd]
        elif 'cygwin' in terminal:
            if not cls.command_exists(cmd):
                print ("ERROR: the command could not be found", cmd)
                return
            else:
                os_command = [cls.command[cls.operating_system()][cmd]]

        if isinstance(arguments, list):
            os_command = os_command + arguments
        elif isinstance(arguments, tuple):
            os_command = os_command + list(arguments)
        elif isinstance(arguments, str):
            os_command = os_command + arguments.split()
        else:
            print ("ERROR: Wrong parameter type", type(arguments))

        result = subprocess.check_output(os_command,
                                         stderr=subprocess.STDOUT).rstrip()

        return result

    @classmethod
    def mkdir(cls, newdir):
        """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
        """
        """http://code.activestate.com/recipes/82465-a-friendly-mkdir/"""
        _newdir = path_expand(newdir)
        if os.path.isdir(_newdir):
            pass
        elif os.path.isfile(_newdir):
            raise OSError("a file with the same name as the desired "
                          "dir, '%s', already exists." % _newdir)
        else:
            head, tail = os.path.split(_newdir)
            if head and not os.path.isdir(head):
                os.mkdir(head)
            if tail:
                os.mkdir(_newdir)


def main():
    shell = Shell()

    print (shell.terminal_type())

    r = shell.execute('pwd')  # copy line replace
    print (r)

    # shell.list()

    # print json.dumps(shell.command, indent=4)

    # test some commands without args
    """
    for cmd in ['whoami', 'pwd']:
        r = shell._execute(cmd)
        print ("---------------------")
        print ("Command: {:}".format(cmd))
        print ("{:}".format(r))
        print ("---------------------")
    """
    r = shell.execute('ls', ["-l", "-a"])
    print (r)

    r = shell.execute('ls', "-l -a")
    print (r)

    r = shell.ls("-aux")
    print (r)

    r = shell.ls("-a", "-u", "-x")
    print (r)

    r = shell.pwd()
    print (r)


if __name__ == "__main__":
    main()
