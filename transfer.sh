#!/bin/bash
set -e

usage () {
  echo "usage: $(basename "$0") remotepath dest"
  exit 1
} >&2

[[ $1 && -d $2 ]] || usage

src=$1
dest=$2
dest_file=$dest/${src##*/}

# store rclone (statically-linked go binary) and config file under shared
# /projects/vla-processing staging area

rclone_base=/projects/vla-processing/measurement_sets/rclone-test

PATH=$PATH:$rclone_base/bin
conf=$rclone_base/config/rclone.conf

rclone lglbs:"$src" "$dest" --config "$conf"

touch "$dest_file.done"

