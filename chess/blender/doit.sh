
set -e

rm -rf renders

export PYTHONPATH=$(pwd)
blender -b --python-exit-code 1 --python-use-system-env --python make.py

blender /tmp/saved.blend -b -f 1