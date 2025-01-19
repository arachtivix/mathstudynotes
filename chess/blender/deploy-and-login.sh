#!/bin/bash

set -e

# Get the instance ID from terraform output
INSTANCE_ID=$(terraform output -raw blender_instance_id)

if [ -z "$INSTANCE_ID" ]; then
    echo "Failed to get instance ID from Terraform output"
    exit 1
fi

echo "Instance ID: $INSTANCE_ID"

# Run the SSM document and capture the command ID
echo "Running SSM setup command..."
COMMAND_ID=$(aws ssm send-command \
    --instance-ids "$INSTANCE_ID" \
    --document-name "setup-blender-environment" \
    --output text \
    --query "Command.CommandId")

if [ -z "$COMMAND_ID" ]; then
    echo "Failed to get command ID from SSM send-command"
    exit 1
fi

echo "Command ID: $COMMAND_ID"

# Wait for the command to complete
echo "Waiting for SSM command to complete..."
aws ssm wait command-executed --command-id "$COMMAND_ID" --instance-id "$INSTANCE_ID"

# Check the command status
COMMAND_STATUS=$(aws ssm list-command-invocations \
    --command-id "$COMMAND_ID" \
    --details \
    --query "CommandInvocations[0].Status" \
    --output text)

if [ "$COMMAND_STATUS" != "Success" ]; then
    echo "SSM command failed with status: $COMMAND_STATUS"
    exit 1
fi

echo "SSM setup completed successfully"

# Execute use-ssm.sh
echo "Running use-ssm.sh..."
./use-ssm.sh
