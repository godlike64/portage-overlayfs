#!/usr/bin/python

import os
import gzip
import logging
import argparse
import sys
import subprocess
import shlex

LOGGER = logging.getLogger("convert_to_ofs")

def setup_logging():
    logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logformat)

def check_overlayfs_support():
    try:
        f = gzip.open('/proc/config.gz', 'r')
        content = f.read()
        return 'CONFIG_OVERLAY_FS=y' in content
    except IOError:
        LOGGER.warning('Could not find /proc/config.gz. Cannot check for overlayfs support reliably!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='convert_to_ofs.py: convert your current portage overlays to Squashfs for use in OverlayFS.')
    parser.add_argument('overlays', type=str, nargs='*', help='Path(s) to current Portage overlay(s)')
    parser.add_argument('-c', '--check', action='store_true', help='Check for OverlayFS support in current kernel. Don\'t do anything else.')
    args = parser.parse_args()
    setup_logging()
    ofs_support = check_overlayfs_support()
    if ofs_support is True:
        LOGGER.info('Current kernel supports Overlay FS support :-)')
    elif ofs_support is False:
        LOGGER.info('Current kernel does NOT support Overlay FS. The initscript may not work!')
    if args.check is True:
        LOGGER.info('Script called with -c/--check. Nothing else to do. Exiting.')
        sys.exit(0)
    COMMAND = 'mksquashfs ORIG DEST -force-uid portage -force-gid portage -comp xz -no-duplicates'
    if args.overlays is None:
        args.overlays = []
    for path in args.overlays:
        if os.path.isdir(path) is True:
            filename = os.path.basename(os.path.normpath(path)) + '.sqfs'
            cmd = COMMAND.replace('ORIG', path).replace('DEST', filename)
            LOGGER.info("Running command: " + cmd)
            pid = subprocess.Popen(shlex.split(cmd))
            pid.wait()
        else:
            LOGGER.error(path + ' is not a path. Skipping')
