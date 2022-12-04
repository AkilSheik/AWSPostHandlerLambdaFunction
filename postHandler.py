import json
import boto3
import time

def lambda_handler(event, context):
    # TODO implement
   ec2 = boto3.resource('ec2')
   region = 'us-east-2'
   all_instances = ec2.instances.filter()
   instance_ids = [instance.id for instance in all_instances]
   client = boto3.client('ssm')
   resp = client.send_command(
       DocumentName="AWS-RunShellScript", # One of AWS' preconfigured documents
       Parameters={'commands': [f". /home/ubuntu/env/bin/activate && python3 /home/ubuntu/send.py '{event}'  "]},
       InstanceIds=['i-0662162c76a7c6c1e'],
    )
    
   command_id = resp['Command']['CommandId']
   time.sleep(2)
   command_invocation_result = client.get_command_invocation(CommandId=command_id, InstanceId="i-0662162c76a7c6c1e")
    

   return {
        'event': event,
        'response': command_invocation_result['StandardErrorContent'],
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'Instance ids': str(instance_ids)
    }
