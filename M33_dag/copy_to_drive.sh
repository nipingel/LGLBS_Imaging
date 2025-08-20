#!/bin/bash
set -e

usage () {
  echo "usage: $(basename "$0") remotepath dest"
  exit 1
} >&2

[[ $1 && -d $2 ]] || usage

src=$1
dest=$2

# store rclone (statically-linked go binary) and config file under shared
staging_dir=/projects/vla-processing/images/M33

rclone_base=/projects/vla-processing/software/rclone

PATH=$PATH:${rclone_base}
conf=${rclone_base}/config/rclone.conf

rclone copy "${staging_dir}/${src}" "${dest}" --config "${conf}"

touch "${dest_file}.done"