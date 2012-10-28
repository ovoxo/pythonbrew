import os
import sys
import subprocess
from pythonbrew.basecommand import Command
from pythonbrew.define import PATH_PYTHONS
from pythonbrew.util import Package
from pythonbrew.log import logger

class PyCommand(Command):
    name = "py"
    usage = "%prog PYTHON_FILE"
    summary = "Runs a named python file against specified and/or all pythonidae"
    
    def __init__(self):
        super(PyCommand, self).__init__()
        self.parser.add_option(
            "-p", "--python",
            dest="pythonidae",
            action="append",
            default=[],
            help="Use the specified python version.",
            metavar='VERSION'
        )
        self.parser.add_option(
            "-v", "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
            help="Show the running python version."
        )
        self.parser.disable_interspersed_args()
    
    def run_command(self, options, args):
        if not args:
            self.parser.print_help()
            sys.exit(1)
        pythonidae = self._get_pythonidae(options.pythonidae)
        for d in pythonidae:
            if options.verbose:
                logger.info('`%s` running...' % d)
            path = os.path.join(PATH_PYTHONS, d, 'bin', args[0])
            if os.path.isfile(path) and os.access(path, os.X_OK):
                subprocess.call([path] + args[1:])
            else:
                path = os.path.join(PATH_PYTHONS, d, 'bin', 'python')
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    subprocess.call([path] + args)
                else:
                    logger.error('%s: No such file or directory.' % path)
    
    def _get_pythonidae(self, _pythonidae):
        pythonidae = [Package(p).name for p in _pythonidae]
        return [d for d in sorted(os.listdir(PATH_PYTHONS))
                if not pythonidae or d in pythonidae]

PyCommand()
