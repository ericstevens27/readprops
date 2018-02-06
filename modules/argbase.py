import json
import sys
from optparse import OptionParser
from sys import platform as _platform

from modules import readbase as rb


class Flags:
    verbose = False
    debug = False
    test = False
    force = False
    config = None
    ubuntu = False
    macos = False
    windows = False
    error = False
    json = False
    id = None
    update = False
    list = False
    type = None
    file = None
    price = 0
    disable = None
    minutes = None
    start = None
    end = None
    configsettings = {}


class MyArgs:
    def __init__(self, use):
        self.usagemsg = use + "\nSee the README file in the project for more details on usage of all programs"

    def __str__(self):
        argstring = "Program Arguments:"
        argstring = argstring + "\nFlags are:\n\tVerbose: {}\n\tDebug: {}\n\tTest: {}\n\tJSON: {}".format(Flags.verbose,
                                                                                                          Flags.debug,
                                                                                                          Flags.test,
                                                                                                          Flags.json)
        argstring = argstring + "\n\tForce: {}\n\tUbuntu: {}\n\tMacOS: {}".format(Flags.force,
                                                                                  Flags.ubuntu,
                                                                                  Flags.macos)
        argstring = argstring + "\n\tId: {}\n\tType: {}\n\tPrice: {}".format(Flags.id, Flags.type, Flags.price)
        argstring = argstring + "\n\tFile: {}".format(Flags.file)
        argstring = argstring + "\nConfig file is [{}]".format(Flags.config)
        argstring = argstring + "\nConfig settings are:\n" + json.dumps(Flags.configsettings, indent=4)
        return argstring

    def processargs(self, opttoset: list):
        """process arguments and options"""
        parser = OptionParser(self.usagemsg)
        parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,
                          help="Print out helpful information during processing")
        parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False,
                          help="Print out debug messages during processing")
        parser.add_option("-t", "--test", dest="test", action="store_true", default=False,
                          help="Use testing server, API and data. "
                               "Also prints out even more information when used with verbose")
        parser.add_option("-j", "--json", dest="json", action="store_true", default=False,
                          help="Output raw JSON from API. Default is a compact, screen friendly display of data.")
        parser.add_option("-c", "--config", dest="config", default="approval_config.json",
                          help="Configuration file (JSON). Default is approval_config.json", metavar="CONFIG")
        if 'f' in opttoset:
            parser.add_option("-f", "--file", dest="file", default=None,
                              help="File (JSON) to use.", metavar="JSON")
        if 'o' in opttoset:
            parser.add_option("-o", "--force", dest="force", action="store_true", default=False,
                              help="Force processing.")
        if 'e' in opttoset:
            parser.add_option("-e", "--disable", dest="disable", default=None,
                              help="Disable. Must be true or false",
                              metavar="TRUE/FALSE")
        if 'm' in opttoset:
            parser.add_option("-m", "--minutes", dest="minutes", default=None, type=int,
                              help="Minutes.",
                              metavar="MINUTES")
        if 'u' in opttoset:
            parser.add_option("-u", "--update", dest="update", action="store_true", default=False,
                              help="Update records. Default is no updates.")
        if 'l' in opttoset:
            parser.add_option("-l", "--list", dest="list", action="store_true", default=False,
                              help="List all build properties")
        if 'i' in opttoset:
            parser.add_option("-i", "--id", dest="id", default=None,
                              help="Build Property Id to use.",
                              metavar="ID")
        if 'y' in opttoset:
            parser.add_option("-y", "--type", dest="type", default=None,
                              help="Type.",
                              metavar="TYPE")
        if 'p' in opttoset:
            parser.add_option("-p", "--price", dest="price", default=0,
                              help="Price.",
                              metavar="PRICE")
        if 's' in opttoset:
            parser.add_option("-s", "--start", dest="start", default=None,
                              help="Start Date for report. Format must be YYYY-MM-DD",
                              metavar="DATE")
        if 'z' in opttoset:
            parser.add_option("-z", "--end", dest="end", default=None,
                              help="End Date for report. Format must be YYYY-MM-DD",
                              metavar="DATE")

        options, args = parser.parse_args()
        # required options checks
        if options.debug:
            options.verbose = True
        Flags.verbose = options.verbose
        Flags.debug = options.debug
        Flags.test = options.test
        Flags.json = options.json
        if 'o' in opttoset:
            Flags.force = options.force
        if 'i' in opttoset:
            Flags.id = options.id
        if 'y' in opttoset:
            Flags.type = options.type
        if 'p' in opttoset:
            Flags.price = options.price
        if 'u' in opttoset:
            Flags.update = options.update
        if 'l' in opttoset:
            Flags.list = options.list
        if 'f' in opttoset:
            Flags.file = options.file
        if 'e' in opttoset:
            Flags.disable = options.disable
        if 'm' in opttoset:
            Flags.minutes = options.minutes
        if 's' in opttoset:
            Flags.start = options.start
        if 'z' in opttoset:
            Flags.end = options.end
        if _platform == "linux" or _platform == "linux2":
            # linux
            Flags.ubuntu = True
        elif _platform == "darwin":
            # MAC OS X
            Flags.macos = True
        else:
            # Windows
            Flags.windows = True
            print('[ERROR]', "Windows is not supported at this time. Please contact eric.stevens@graphitesoftware.com")
            sys.exit(2)

        Flags.config = options.config
        if Flags.config is not None:
            cf = rb.ReadJson('.', '.', Flags.config)
            cf.readinput()
            Flags.configsettings = cf.data
        else:
            print('[ERROR]', "Missing required configuration file (--config)")
            sys.exit(2)


# noinspection PyMethodMayBeStatic,PyPep8Naming
class MSG:
    def ERROR(self, msg):
        print('[ERROR]', msg)
        sys.exit(2)

    def WARNING(self, msg):
        print('[WARNING]', msg)

    def VERBOSE(self, msg):
        if Flags.verbose:
            print(msg)

    def DEBUG(self, msg):
        if Flags.debug:
            print('[DEBUG]', msg)

    def TEST(self, msg):
        if Flags.test and Flags.verbose:
            print('[TEST]', msg)


def displaycounter(message: list, count: list):
    """provides a pretty counter style display for things like records processed"""
    display = "\r"
    for m in message:
        # print (message.index(m))
        display = display + m + " {" + str(message.index(m)) + ":,d} "
        # print (display)
    print(display.format(*count), end='')
