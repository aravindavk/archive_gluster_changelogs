#!/usr/bin/python3
import sys
import xattr
import struct
import os
import shutil
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
import configparser

GLUSTERFIND_DIR = "/var/lib/glusterd/glusterfind"
config = configparser.ConfigParser()

def move_changelog(to_dir, changelog_file):
    shutil.move(changelog_file, to_dir)


def get_glusterfind_time(brick_path):
    status_file = "{0}.status".format(urllib.parse.quote_plus(brick_path))
    stimes = []

    # Each session Dir
    for session in os.listdir(GLUSTERFIND_DIR):
        full_path = os.path.join(GLUSTERFIND_DIR, session)
        if os.path.isdir(full_path):
            # Each volume directory in session dir
            for v in os.listdir(full_path):
                full_path_2 = os.path.join(full_path, v)
                if os.path.isdir(full_path_2):
                    # Each file in session dir and match for brick status file
                    for f in os.listdir(full_path_2):
                        if f == status_file:
                            with open(os.path.join(full_path_2, f)) as sf:
                                stimes.append(int(sf.read()))

    if stimes:
        return min(stimes)


def get_archive_stime(brick_path):
    """
    When removing georep sessions dangling stimes will remain with a value of "0"
    We want to avoid them , so we check for the stime-xattr-prefix in each gsyncd.conf
    Then we get the minimum stime
    """
    xattrs_list = []
    for path in Path('/var/lib/glusterd/geo-replication/').rglob('gsyncd.conf'):
        config.read(path)
        #print(f"Reading stime prefix { config['vars']['stime-xattr-prefix'] } from file { path }")
        xattrs_list.append(config['vars']['stime-xattr-prefix'] + '.stime')

    stime_xattr_values = []
    for x in xattrs_list:
        stime = struct.unpack("!II", xattr.getxattr(brick_path, x))
        stime_xattr_values.append(stime[0])

    if stime_xattr_values:
        return min(stime_xattr_values)
    else:
        return 0


def main(brick_path, archive_dir):
    stime = get_archive_stime(brick_path)
    glusterfind_time = get_glusterfind_time(brick_path)
    if glusterfind_time is not None:
        stime = min(stime, glusterfind_time)

    changelogs_dir = os.path.join(brick_path, ".glusterfs/changelogs")
    for cf in Path(changelogs_dir).rglob('CHANGELOG.*'):
            cf_ts = int(cf.name.split(".")[-1])
            if cf_ts < stime:
                move_changelog(archive_dir, os.path.join(changelogs_dir, cf))
                print("Archived: {0}".format(cf))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

