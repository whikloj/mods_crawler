#!/usr/bin/env python3

import argparse
import os
import os.path
from xml.etree import ElementTree
import hashlib
import urllib.parse

namespaces = {
    'foxml': 'info:fedora/fedora-system:def/foxml#',
    'audit': 'info:fedora/fedora-system:def/audit#',
    'xsl': 'http://www.w3.org/2001/XMLSchema-instance',
    }
xpaths = {}

strip_attribs = [
    'VALUE'
]
config = {}

def process_attribs(attribs):
    output = []
    for (attrib, value) in attribs.items():
        if not attrib.upper() in strip_attribs:
            output.append("@{0}=\"{1}\"".format(attrib, value))
    return output


def process_path(node, path=''):
    global xpaths
    attribs = process_attribs(node.attrib)
    attrib_string = ''
    if len(attribs) > 0:
        attrib_string = "[{0}]".format(" and ".join(attribs))
    element = "{0}{1}".format(node.tag, attrib_string)
    if len(node) > 0:
        for child in node:
            process_path(child, path + '/' + element)
    else:
        if path not in xpaths.keys():
            xpaths[path] = 1
        else:
            xpaths[path] += 1


def get_mods(tree):
    results = tree.findall('.//foxml:datastream[@ID="MODS"]', namespaces)
    for result in results:
        if 'CONTROL_GROUP' in result.attrib and result.attrib['CONTROL_GROUP'] == 'X':
            '''Inline XML'''
            mods = result.find('.//foxml:datastreamVersion[position() == last()]/foxml:xmlContent', namespaces)
            if mods is not None:
                return mods
        elif 'CONTROL_GROUP' in result.attrib and result.attrib['CONTROL_GROUP'] == 'M':
            versions = result.findall('.//foxml:datastreamVersion', namespaces)
            if versions is not None:
                current_version_number = 0
                for version in versions:
                    (dsID, check_version) = version.attrib['ID'].split('.')
                    if int(check_version) > current_version_number:
                        current_version_number = int(check_version)
                final_version = result.find("./foxml:datastreamVersion[@ID='{0}.{1}']".format(
                                                   dsID,
                                                   current_version_number
                                               ) +
                                               "/foxml:contentLocation[@TYPE='INTERNAL_ID']", namespaces)
                if final_version is not None:
                    mods_location = final_version.attrib['REF']
                    if not mods_location.startswith("info:fedora/"):
                        mods_location = "info:fedora/{0}".format(mods_location)
                    mods_location = mods_location.replace("+", "/")
                    mods_hash = hashlib.md5(mods_location.encode('UTF-8')).hexdigest()[:config.hash_length]
                    mods_location = urllib.parse.quote(mods_location, '')
                    mods_file_location = os.path.join(config.datastreamstore, mods_hash, mods_location)

                    if not os.path.exists(mods_file_location):
                        print("Unable to find MODS file at {0}".format(mods_file_location))
                        return None
                    else:
                        with open(mods_file_location, 'rt') as f:
                            for (prefix, uri) in namespaces.items():
                                ElementTree.register_namespace(prefix, uri)
                            tree = ElementTree.parse(f)
                            return tree.getroot()


def start(args):
    global config
    config = args
    for (dirpath, dirnames, filenames) in os.walk(config.objectstore):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            print("Processing objectstore file {}".format(filepath))
            with open(filepath, 'rt') as f:
                if filepath.endswith("info%3Afedora%2Fislandora%3A8"):
                    pass
                for (prefix, uri) in namespaces.items():
                    ElementTree.register_namespace(prefix, uri)
                tree = ElementTree.parse(f)
                mods = get_mods(tree)
                if mods is not None:
                    process_path(mods)
                else:
                    continue
    print()
    for (xpath, count) in xpaths.items():
        print("XPath {0} was used {1} times".format(xpath, count))
    print("\nDone")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Iterates over files in a Fedora 3 objectStore to locate all MODS datastreams and count distinct XPaths")
    parser.add_argument('-o', '--objectstore', dest='objectstore', help="Location of the Fedora3 object store")
    parser.add_argument('-d', '--datastreamstore', dest='datastreamstore', help="Location of the Fedora3 datastream store")
    parser.add_argument('-l', '--hash_length', dest="hash_length", default=2, type=int, help="Integer length of the configured hash (defaults to 2)")
    args = parser.parse_args()
    args.objectstore = os.path.realpath(args.objectstore)
    args.datastreamstore = os.path.realpath(args.datastreamstore)
    if not os.path.exists(args.objectstore):
        parser.error("Object store path not found ({})".format(args.objectstore))
    elif not os.path.exists(args.datastreamstore):
        parser.error("Datastream store path not found ({})".format(args.datastreamstore))
    start(args)
