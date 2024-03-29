#!/usr/bin/env python
"""
Usage:
	plasmasetconfig # List all widget namespaces
	plasmasetconfig org.kde.plasma.digitalclock # List all config groups+keys
	plasmasetconfig org.kde.plasma.digitalclock Appearance showSeconds true
Install:
	chmod +x ~/Downloads/plasmasetconfig.py
	sudo cp ~/Downloads/plasmasetconfig.py /usr/local/bin/plasmasetconfig
Uninstall:
	sudo rm /usr/local/bin/plasmasetconfig
"""

# credit goes to Zren https://gist.github.com/Zren/764f17c26be4ea0e088f4a6a1871f528 give him a star!!

import argparse
import dbus
import os
import re
import subprocess
import sys


def writeConfigKey(args):
    widgetType = args.widget or ""
    configGroup = args.group or ""
    configKey = args.key or ""
    configValue = args.value or ""

    # print("widgetType", widgetType)
    # print("configGroup", configGroup)
    # print("configKey", configKey)
    # print("configValue", configValue)

    # https://userbase.kde.org/KDE_System_Administration/PlasmaDesktopScripting
    plasmaScript = """
	function forEachWidgetInContainment(containment, callback) {
		var widgets = containment.widgets();
		for (var widgetIndex = 0; widgetIndex < widgets.length; widgetIndex++) {
			var widget = widgets[widgetIndex];
			callback(widget, containment);

			if (widget.type == "org.kde.plasma.systemtray") {
				var childContainmentId = widget.readConfig("SystrayContainmentId");
				if (typeof childContainmentId !== "undefined") {
					var childContainment = desktopById(childContainmentId);
					if (typeof childContainment !== "undefined" && childContainment.type == "org.kde.plasma.private.systemtray") {
						forEachWidgetInContainment(childContainment, callback);
					}
				}
			}
		}
	}

	function forEachWidgetInContainmentList(containmentList, callback) {
		for (var containmentIndex = 0; containmentIndex < containmentList.length; containmentIndex++) {
			var containment = containmentList[containmentIndex];
			forEachWidgetInContainment(containment, callback);
		}
	}

	function forEachWidget(callback) {
		forEachWidgetInContainmentList(desktops(), callback);
		forEachWidgetInContainmentList(panels(), callback);
	}

	function forEachWidgetByType(type, callback) {
		forEachWidget(function(widget, containment) {
			if (widget.type == type) {
				callback(widget, containment);
			}
		});
	}

	function widgetSetProperty(args) {
		if (!(args.widgetType && args.configGroup && args.configKey)) {
			return;
		}
		forEachWidgetByType(args.widgetType, function(widget){
			widget.currentConfigGroup = [args.configGroup];
			widget.writeConfig(args.configKey, args.configValue);
			var newValue = widget.readConfig(args.configKey);
		});
	}


	var args = {
		widgetType: "{{widgetType}}",
		configGroup: "{{configGroup}}",
		configKey: "{{configKey}}",
		configValue: "{{configValue}}",
	}
	widgetSetProperty(args);
	"""

    plasmaScript = plasmaScript.replace("\n", " ")
    plasmaScript = plasmaScript.replace("{{widgetType}}", widgetType)
    plasmaScript = plasmaScript.replace("{{configGroup}}", configGroup)
    plasmaScript = plasmaScript.replace("{{configKey}}", configKey)
    plasmaScript = plasmaScript.replace("{{configValue}}", configValue)

    # print(plasmaScript)

    # https://dbus.freedesktop.org/doc/dbus-python/tutorial.html
    # qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript ""
    session_bus = dbus.SessionBus()
    plasmashell_obj = session_bus.get_object("org.kde.plasmashell", "/PlasmaShell")
    plasmashell = dbus.Interface(plasmashell_obj, dbus_interface="org.kde.PlasmaShell")
    plasmashell.evaluateScript(plasmaScript)


# --- Package config/main.xml Parser
packageDirList = [
    os.path.expanduser("~/.local/share/plasma/plasmoids"),
    "/usr/share/plasma/plasmoids",
    os.path.expanduser("~/.local/share/plasma/wallpapers"),
    "/usr/share/plasma/wallpapers",
]


def findWidgetDir(namespace):
    for packageDir in packageDirList:
        filepath = os.path.join(packageDir, namespace)
        if os.path.isdir(filepath):
            return filepath

    return None


def getEntryLabel(text):
    pattern = r"<label>(.+?)<\/label>"
    return m.group(1) if (m := re.search(pattern, text)) else None


def getEntryDefault(text):
    pattern = r"<default>(.+?)<\/default>"
    return m.group(1) if (m := re.search(pattern, text)) else None


def getChoiceList(text):
    pattern = r"<choice ([^>]+)(\/>|>(.+?)<\/choice>)"
    choiceList = []
    for m in re.finditer(pattern, text, flags=re.DOTALL):
        # print(m)
        attrXml = m.group(1)
        choiceName = getXmlAttr(attrXml, "name")
        choiceList.append(choiceName)
    return choiceList


def getEntryChoices(text):
    pattern = r"<choices>(.+?)<\/choices>"
    if m := re.search(pattern, text, flags=re.DOTALL):
        return getChoiceList(m[1])
    else:
        return None


def getXmlAttr(text, key):
    pattern = key + r"\s*=\s*\"([^\">]+)\""  # There's unlikely to be escaped quotes
    return m.group(1) if (m := re.search(pattern, text)) else None


def iterGroupEntry(text):
    pattern = r"<entry ([^>]+)>(.+?)<\/entry>"
    for m in re.finditer(pattern, text, flags=re.DOTALL):
        # print(m)
        attrXml = m.group(1)
        innerXml = m.group(2)
        yield {
            "name": getXmlAttr(attrXml, "name"),
            "type": getXmlAttr(attrXml, "type"),
            "default": getEntryDefault(innerXml),
            "label": getEntryLabel(innerXml) or "",
            "choices": getEntryChoices(innerXml),
        }


def iterGroup(text):
    pattern = r"<group ([^>]+)>(.+?)<\/group>"
    for m in re.finditer(pattern, text, flags=re.DOTALL):
        # print(m)
        attrXml = m.group(1)
        innerXml = m.group(2)
        # print('group', attrXml)
        group = {
            "name": getXmlAttr(attrXml, "name"),
            "entries": [],
        }

        for entry in iterGroupEntry(innerXml):
            group["entries"].append(entry)

        yield group


# --- Terminal Colors
class TC:
    RESET = "\033[0m"
    FG_BLACK = "\033[30m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[32m"
    FG_ORANGE = "\033[33m"
    FG_BLUE = "\033[34m"
    FG_PURPLE = "\033[35m"
    FG_CYAN = "\033[36m"
    FG_LIGHTGREY = "\033[37m"
    FG_DARKGREY = "\033[90m"
    FG_LIGHTRED = "\033[91m"
    FG_LIGHTGREEN = "\033[92m"
    FG_YELLOW = "\033[93m"
    FG_LIGHTBLUE = "\033[94m"
    FG_PINK = "\033[95m"
    FG_LIGHTCYAN = "\033[96m"


def prettyValue(value):
    if value is None:
        return '""'
    if " " in value:
        return '"' + value.replace('"', '\\"') + '"'
    else:
        return value.replace('"', '\\"')


def formatEntryType(entry):
    if entry["choices"] is not None:
        return f'{entry["type"]} {", ".join(f"{i}={key}" for i, key in enumerate(entry["choices"]))}'

    else:
        return entry["type"]


def printConfigKey(namespace, group, entry, showLabel=False):
    line = ""
    if showLabel:
        line += "".join(
            [
                f"{TC.FG_DARKGREY}# {entry['label']}{TC.RESET}\n",
                "plasmasetconfig",
                f" {TC.FG_PINK}{namespace}",
                f" {TC.FG_LIGHTBLUE}{prettyValue(group['name'])}",
                f" {TC.FG_LIGHTGREEN}{prettyValue(group['name'])}",
                f" {TC.FG_YELLOW}{prettyValue(entry['default'])}",
                f" {TC.FG_DARKGREY}# {formatEntryType(entry)}",
                TC.RESET,
            ]
        )
    print(line)


def printPackageConfigKeys(namespace, showLabels=False):
    packageDir = findWidgetDir(namespace)
    if packageDir is None:
        print(f'Could not find a package with the namespace "{namespace}"')
        sys.exit(1)

    configPath = os.path.join(packageDir, "contents/config/main.xml")

    if not os.path.isfile(configPath):
        print(f'Package at "{packageDir}" does not contain "contents/config/main.xml"')
        sys.exit(1)

    with open(configPath, "r") as fin:
        text = fin.read()

    for group in iterGroup(text):
        for entry in group["entries"]:
            printConfigKey(namespace, group, entry, showLabel=showLabels)


def printPackage(namespace, dirpath):
    line = "".join(
        [
            "plasmasetconfig",
            f" {TC.FG_PINK}{namespace}",
            f" {TC.FG_DARKGREY}# {dirpath}",
            TC.RESET,
        ],
    )
    print(line)


def printNamespaceList():
    namespaceList = set()
    for packageDir in packageDirList:
        if os.path.isdir(packageDir):
            for filename in sorted(os.listdir(packageDir)):
                filepath = os.path.join(packageDir, filename)
                if os.path.isdir(filepath) and filename not in namespaceList:
                    namespaceList.add(filename)
                    printPackage(filename, packageDir)


# --- Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print config key labels"
    )
    parser.add_argument(
        "widget", type=str, help="widget namespace eg: 'org.kde.plasma.digitalclock'"
    )
    parser.add_argument("group", type=str, help="config group")
    parser.add_argument("key", type=str, help="config key to modify")
    parser.add_argument("value", type=str, help="new value to store in config key")

    # Note: "plasmasetconfig.py" is first "arg"
    flagArgs = list(filter(lambda s: s.startswith("-"), sys.argv))
    posArgs = list(filter(lambda s: not s.startswith("-"), sys.argv))
    numPosArgs = len(posArgs)

    if numPosArgs == 1:
        # plasmasetconfig
        parser.print_usage()
        print()
        printNamespaceList()
        sys.exit(1)
    elif numPosArgs in {2, 3}:
        # plasmasetconfig [widget]
        # plasmasetconfig [widget] [group]
        widget = posArgs[1]
        verbose = "-v" in flagArgs or "--verbose" in flagArgs
        parser.print_usage()
        print()
        printPackageConfigKeys(widget, showLabels=verbose)
        sys.exit(1)

    args = parser.parse_args()
    writeConfigKey(args)
