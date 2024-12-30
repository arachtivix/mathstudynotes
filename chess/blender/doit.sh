
export PYTHONPATH=$(pwd)
blender --debug --python-exit-code 1 --python-use-system-env --python make.py
# render does not have to be separate, but it may help with stuff
blender /tmp/saved.blend -b -a --threads 15