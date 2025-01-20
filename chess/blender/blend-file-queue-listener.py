#!/usr/bin/python3

import boto3
import time
import json


client = boto3.client("sqs", region_name="us-east-1")


while True:
    message = client.receive_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/650354402179/wernerware-gen-blends",
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10)
    filename = f"/var/wernerware/sqs_reporter/report_{str(time.now())}.txt"
    with open(filename, "w") as f:
        f.write(json.dumps(message))
    time.sleep(10) # let's just make sure I don't spam sqs