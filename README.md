# Tool to archive Gluster Changelogs
Changelogs are not required for Geo-replication once the Changelogs
are consumed and synced to Slave. This tool helps to archive the
changelogs which are already consumed.

## NOTE:

- Do not use this tool if `glusterfind` or any other tools are
  used with Volume(Tools which consumes Changelogs other than
  Geo-replication)
- Use this tool only when all the Geo-rep sessions are in Changelog
  mode(Geo-rep Status will show this information)

## Usage

    mkdir <archive_dir>
    python main.py <brick_path> <archive_dir>
    cd <archive_dir>
    tar cvzf <archive>.tar.gz <archive>/

Example:

    mkdir /backups/changelogs_bricks_b1_20170119
    python main.py /bricks/b1 /backups/changelogs_bricks_b1_20170119
    cd /backups/
    tar cvzf changelogs_bricks_b1_20170119.tar.gz changelogs_bricks_b1_20170119

## How it works?

- List xattrs for given brick path
- If xattr name ends with `.stime`, read the xattr value(Repeat this
  for all the stime xattrs)
- Archive all changelogs files if Changelog file Timestamp is less
  than min of stime values collected in previous step.
