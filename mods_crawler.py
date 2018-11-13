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
    """Make attributes clean for printing and strip values."""
    output = []
    for (attrib, value) in attribs.items():
        if not attrib.upper() in strip_attribs:
            output.append("@{0}=\"{1}\"".format(attrib, value))
    return output


def process_path(node, path=''):
    """Somewhat recursive function to build XPaths."""
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


def get_last_version(element):
    """Get the last version of a datastream by comparing ID numbers."""
    versions = element.findall('.//foxml:datastreamVersion', namespaces)
    if versions is not None:
        current_version_number = 0
        for version in versions:
            (dsID, check_version) = version.attrib['ID'].split('.')
            if int(check_version) > current_version_number:
                current_version_number = int(check_version)
        return element.find("./foxml:datastreamVersion[@ID='{0}.{1}']".format(
            dsID,
            current_version_number
        ), namespaces)
    return None


def get_mods(tree):
    """Get the MODS record either out of the Inline XML or from a managed file."""
    results = tree.findall('.//foxml:datastream[@ID="MODS"]', namespaces)
    for result in results:
        if 'CONTROL_GROUP' in result.attrib and result.attrib['CONTROL_GROUP'] == 'X':
            '''Inline XML'''
            mods = get_last_version(result)
            if mods is not None:
                return mods.find('./foxml:xmlContent', namespaces)
        elif 'CONTROL_GROUP' in result.attrib and result.attrib['CONTROL_GROUP'] == 'M':
            final_version = get_last_version(result)
            if final_version is not None:
                final_version_content = final_version.find("./foxml:contentLocation[@TYPE='INTERNAL_ID']", namespaces)
                if final_version_content is not None:
                    mods_location = final_version_content.attrib['REF']
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
                            try:
                                tree = ElementTree.parse(f)
                                return tree.getroot()
                            except ElementTree.ParseError:
                                print("Error parsing {0}, may not be XML. Skipping".format(mods_file_location))
                                return None


def start(args):
    """Starter iterates all files in the objectStore directory."""
    setup(args)
    for (dirpath, dirnames, filenames) in os.walk(config.objectstore):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            if allowed_prefix(file):
                print("Processing objectstore file {}".format(filepath))
                with open(filepath, 'rt') as f:
                    for (prefix, uri) in namespaces.items():
                        ElementTree.register_namespace(prefix, uri)

                    try:
                        tree = ElementTree.parse(f)
                        mods = get_mods(tree)
                    except ElementTree.ParseError:
                        print("Error parsing {0}, may not be XML. Skipping".format(filepath))
                        mods = None

                    if mods is not None:
                        process_path(mods)
                    else:
                        continue
            else:
                print("Skipping {0} due to namespace restrictions.".format(filepath))
    print()
    for (xpath, count) in xpaths.items():
        print("XPath {0} was used {1} times".format(xpath, count))
    print("\nDone")


def allowed_prefix(filename):
    """Check the filename against the allowed list."""
    for ns in config.allowed_namespaces:
        if filename.startswith(ns):
            return True
    return False


def prefix_filename(filename):
    """Adds the encoded info:fedora/ prefix if needed"""
    if not (filename.startswith("info:fedora/") or filename.startswith("info%3Afedora%2F")):
        return urllib.parse.quote("info:fedora/" + filename, '')
    return filename


def setup(args):
    """Any global configuration things."""
    global config
    config = args
    if config.allowed_namespaces is None:
        config.allowed_namespaces = ['islandora']
    else:
        config.allowed_namespaces = config.allowed_namespaces.split(',')
    config.allowed_namespaces = [prefix_filename(x) for x in config.allowed_namespaces]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Iterates over files in a Fedora 3 objectStore to locate all MODS datastreams and count distinct XPaths")
    parser.add_argument('-o', '--objectstore', dest='objectstore', help="Location of the Fedora3 object store")
    parser.add_argument('-d', '--datastreamstore', dest='datastreamstore', help="Location of the Fedora3 datastream store")
    parser.add_argument('-l', '--hash_length', dest="hash_length", default=2, type=int, help="Integer length of the configured hash (defaults to 2)")
    parser.add_argument('-n', '--namespaces', dest="allowed_namespaces", help="Comma delimited list of namespaces to parse, defaults to \"islandora\"")
    args = parser.parse_args()
    args.objectstore = os.path.realpath(args.objectstore)
    args.datastreamstore = os.path.realpath(args.datastreamstore)
    if not os.path.exists(args.objectstore):
        parser.error("Object store path not found ({})".format(args.objectstore))
    elif not os.path.isdir(args.objectstore):
        parser.error("Object store path is not a directory ({})".format(args.objectstore))
    elif not os.path.exists(args.datastreamstore):
        parser.error("Datastream store path not found ({})".format(args.datastreamstore))
    elif not os.path.isdir(args.datastreamstore):
        parser.error("Datastream store path is not a directory ({})".format(args.datastreamstore))
    start(args)
