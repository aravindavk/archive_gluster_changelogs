#!/usr/bin/env python
import sys
import xattr
import struct
import os
import shutil


def move_changelog(to_dir, changelog_file):
    shutil.move(changelog_file, to_dir)


def get_archive_stime(brick_path):
    """
    Get all stime xattrs and find minimum stime
    """
    stime_xattr_values = []
    xattrs_list = xattr.list(brick_path)
    for x in xattrs_list:
        if x.endswith(".stime"):
            stime = struct.unpack("!II", xattr.get(brick_path, x))
            stime_xattr_values.append(stime[0])

    if stime_xattr_values:
        return min(stime_xattr_values)
    else:
        return 0


def main(brick_path, archive_dir):
    stime = get_archive_stime(brick_path)
    changelogs_dir = os.path.join(brick_path, ".glusterfs/changelogs")
    for cf in os.listdir(changelogs_dir):
        if cf.startswith("CHANGELOG."):
            cf_ts = int(cf.split(".")[-1])
            if cf_ts < stime:
                move_changelog(archive_dir, os.path.join(changelogs_dir, cf))
                print "Archived: {0}".format(cf)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
