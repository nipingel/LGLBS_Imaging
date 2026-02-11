#!/bin/bash
src=$1
dest=$2

# store rclone (statically-linked go binary) and config file under shared
staging_dir=/projects/vla-processing/images/M33

rclone_base=/projects/vla-processing/software/rclone

PATH=$PATH:${rclone_base}
conf=${rclone_base}/rclone.conf

echo "here"
rclone copy "${staging_dir}/${src}" "${dest}" --config "${conf}"

touch "${src}.done"
