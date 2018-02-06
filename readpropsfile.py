#!/usr/local/bin/python3

import re
import json
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
    do.processargs(['i', 'l'])
    if arg.Flags.test:
        msg.TEST("Running in test mode.")
    msg.DEBUG(do)
    bp = rb.ReadJson(arg.Flags.configsettings['root'], arg.Flags.configsettings['data'], arg.Flags.configsettings['propsfile'])
    bp.readinput()
    if arg.Flags.json:
        msg.VERBOSE("Dumping full JSON of build properties file")
        print(json.dumps(bp.data, indent=2, ensure_ascii=False ))
    if arg.Flags.id and arg.Flags.list:
        msg.VERBOSE("Searching for instances of property {}".format(arg.Flags.id))
        # count property
        propscount = 0
        devicecount = 0
        for tag, data in bp.data.items():
            devicecount += 1
            for p in data['props']:
                if p == arg.Flags.id:
                    propscount += 1
        print("There are {} out of {} devices with the property {}".format(propscount, devicecount, arg.Flags.id))
    elif arg.Flags.id is None or arg.Flags.list:
        msg.VERBOSE("Showing list of properties")
        # assemble property list
        props = []
        for tag, data in bp.data.items():
            for p in data['props']:
                if p not in props:
                    props.append(p)
        for p in props:
            print(p)
    else:
        msg.VERBOSE("Showing all instances of property {}".format(arg.Flags.id))
        for tag, data in bp.data.items():
            if arg.Flags.id in data['props']:
                print("{} {} [MIUI {}] {} is {}".format(data['model'], data['region'], data['version'], arg.Flags.id, data['props'][arg.Flags.id]))
            else:
                print("{} {} [MIUI {}] {} missing for this model".format(data['model'], data['region'], data['version'], arg.Flags.id))


def extractgroup(match):
    """extract the group (index: 1) from the match object"""
    if match is None:
        return None
    return match.group(1)


if __name__ == '__main__':
    main()
