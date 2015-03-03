# portage-overlayfs
Keep your portage tree in an OverlayFS/SquashFS

## Purpose

The purpose of this is mainly to learn, and also to replay any scripts you might have currently using AUFS or similar filesystems. Since OverlayFS entered the Linux kernel tree, I think it's unlikely that AUFS will ever get in. Furthermore, OverlayFS is more powerful and actively developed.

## Usage

Just dump both files in the according directories (*/etc/init.d/overlay* for the initscript, */etc/conf.d/overlay* for the configuration file), edit the conf.d file accordingly and start the service.

**Note: you must have valid images at the specified path and name for the script to work.**

## TODO

- A script to convert your current trees into suitable squash images.

## Credits

Original credits go to Mathias Laurin for the */etc/init.d/squashfs_portage* script, which used a combination of AUFS + SquashFS.
