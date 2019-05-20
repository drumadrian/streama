import boto3
import os

#################################################################
# Global Flags
#################################################################
DEBUG = True

#################################################################
# ToDo:
#   Include notification on job submission 
#################################################################

#################################################################
# Outline

# Extract s3 object name
# Create Elastic Transcoder job
#################################################################

#################################################################
# Create Elastic Transcoder job
#################################################################

def start_transcode(input_raw_s3_object_list, input_pipeline_id):

    client = boto3.client('elastictranscoder')

    for input_filename in input_raw_s3_object_list:

        new_s3_key = '.'.join(input_filename.split('.')[:-1]) + '.mp3'

        if DEBUG:
            print("\nnew_s3_key={}\n".format(new_s3_key))

        client.create_job(
            PipelineId=input_pipeline_id,
            Input={
                'Key': input_filename
                # 'FrameRate': 'auto',
                # 'Resolution': 'auto',
                # 'AspectRatio': 'auto',
                # 'Interlaced': 'auto',
                # 'Container': 'auto'
            },
            Outputs=[{
                'Key': new_s3_key,
                'PresetId': '1351620000001-300010'
            }]
        )

        print("Started transcoding {0}".format(input_filename))


#################################################################
# Extract s3 object name
#################################################################

def extract_s3_object_list(received_event):

    list_of_s3_object_records = received_event['Records']

    list_of_s3_object_names = []

    for record in list_of_s3_object_records:
        next_object = record['s3']['object']['key']
        list_of_s3_object_names.append(next_object)
        if DEBUG:
            print("Appended object: {}".format(next_object))

    return list_of_s3_object_names


#remove function 
def get_fake_input():

    fake_input = {
      "Records": [
        {
          "eventVersion": "2.0",
          "eventTime": "1970-01-01T00:00:00.000Z",
          "requestParameters": {
            "sourceIPAddress": "127.0.0.1"
          },
          "s3": {
            "configurationId": "testConfigRule",
            "object": {
              "eTag": "0123456789abcdef0123456789abcdef",
              "sequencer": "0A1B2C3D4E5F678901",
              "key": "remix1.m4a",
              "size": 1024
            },
            "bucket": {
              "arn": "arn:aws:s3:::83pluspro-raw-recordings",
              "name": "83pluspro-raw-recordings",
              "ownerIdentity": {
                "principalId": "EXAMPLE"
              }
            },
            "s3SchemaVersion": "1.0"
          },
          "responseElements": {
            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
            "x-amz-request-id": "EXAMPLE123456789"
          },
          "awsRegion": "us-east-1",
          "eventName": "ObjectCreated:Put",
          "userIdentity": {
            "principalId": "EXAMPLE"
          },
          "eventSource": "aws:s3"
        }
      ]
    }

    return fake_input






def lambda_handler(event, context):
    
    # input_event =  get_fake_input()
    # event = input_event

    pipeline_id = os.environ['target_pipeline_id']

    if DEBUG:
        print("\n Received event={}".format(event))
    
    raw_s3_object_list = extract_s3_object_list(event)

    start_transcode(raw_s3_object_list, pipeline_id)


    return 'transcode_lambda_function() complete'




