#!/bin/sh

set -ex

echo Backing up emacs configs
rm ./*.el
cp ~/.emacs.d/*.el .
