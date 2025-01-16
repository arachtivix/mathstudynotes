#!/bin/bash

set -e

INSTANCE_ID=$(terraform output --raw blender_instance_id)

#!/bin/bash

set -e

aws ssm start-session --target ${INSTANCE_ID}