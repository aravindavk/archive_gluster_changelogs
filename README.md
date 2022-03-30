# Tool to archive Gluster Changelogs
Changelogs are not required for Geo-replication once the Changelogs
are consumed and synced to Slave. This tool helps to archive the
changelogs which are already consumed.

## NOTE:

- If Geo-replication is used, use this tool only when all the Geo-rep
  sessions are in Changelog mode(Geo-rep Status will show this
  information)

  Note: In archive_georep_changelogs_p3.py this check is in the script

## REQUIREMENTS
- python2:
  * xattr
- python3:
  * xattr
  * glustercli

## Usage

    # When using python2
    mkdir <archive_dir>
    python2 archive_georep_changelogs_p2.py <brick_path> <archive_dir>
    cd <archive_dir>
    tar cvzf <archive>.tar.gz <archive>/

    # When using python3
    mkdir <archive_dir>
    python3 archive_georep_changelogs_p3.py <brick_path> <archive_dir>

Example:

    mkdir /backups/changelogs_bricks_b1_20170119
    python3 archive_georep_changelogs_p3.py /bricks/b1 /backups/changelogs_bricks_b1_20170119

## How it works?

- List xattrs for given brick path
- If xattr name ends with `.stime`, read the xattr value(Repeat this
  for all the stime xattrs)
- Gets Timestamp from brick status files of Glusterfind
- Archive all changelogs files if Changelog file Timestamp is less
  than min of stime values collected in previous steps.
- The python3 version of the script creates a tgz archive and adds all changelog files to it.
