#!/usr/local/bin/python3

import re
from modules import readbase as rb

from modules import argbase as arg

# define global variables

# options as globals
usagemsg = "This program reads the JSON file for specific fields"
msg = arg.MSG()
re_miui = r"Stable(.*?).build.prop$"
re_modelchina = r"(.*?)ChinaStable"
re_modelglobal = r"(.*?)GlobalStable"


def main():
    """main processing loop"""
    do = arg.MyArgs(usagemsg)
    do.processargs(['i'])
    if arg.Flags.test:
        msg.TEST("Running in test mode.")
    msg.DEBUG(do)
    bp = rb.ReadJson(arg.Flags.configsettings['root'], arg.Flags.configsettings['data'], arg.Flags.configsettings['propsfile'])
    bp.readinput()
    if arg.Flags.id is None:
        msg.ERROR("You must specifcy a property to show using the --id option")
    for prop, data in bp.data.items():
        miui = extractgroup(re.search(re_miui, prop))
        modelc = extractgroup(re.search(re_modelchina, prop))
        modelg = extractgroup(re.search(re_modelglobal, prop))
        if modelg:
            model = modelg + " (Global)"
        else:
            model = modelc + " (China)"
        if arg.Flags.id in data['props']:
            print("{} [MIUI {}] {} is {}".format(model, miui, arg.Flags.id, data['props'][arg.Flags.id]))
        else:
            print("{} [MIUI {}] {} missing for this model".format(model, miui, arg.Flags.id))


def extractgroup(match):
    """extract the group (index: 1) from the match object"""
    if match is None:
        return None
    return match.group(1)


if __name__ == '__main__':
    main()
