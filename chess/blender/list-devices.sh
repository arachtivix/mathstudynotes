
set -e

export PYTHONPATH=$(pwd)
blender --debug --background --python-exit-code 1 --python-use-system-env --python list-devices.py