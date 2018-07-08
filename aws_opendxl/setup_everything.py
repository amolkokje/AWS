import os
import boto3
from moto import mock_s3, mock_ecs, mock_ec2, mock_cloudformation


# Broker/
# SNS triggers Lambda
# Lambda has DXL client which connects to the broker and sends event /dxl/test/event

# 

@mock_s3
@mock_ec2
@mock_ecs
@mock_cloudformation
def main():
    s3_client = boto3.client('s3')
    ec2_client = boto3.client('ec2')
    ecs_client = boto3.client('ecs')
    
    pass


def deploy_dxlbroker(client):
    print 'Deploying dxlbroker container ...'
    cluster_name = 'test_cluster'
    task_def_name = 'test_task_def'
    task_name = 'test_task'
            
    client.create_cluster(clusterName=cluster_name)
    
    client.register_task_definition(
		family=task_def_name,
		containerDefinitions=[
			{
				'name': 'test_container',
				'image': 'amolkokje/opendxl-environment-centos',
				'portMappings': [
					{
						'containerPort': 8000,
						'hostPort': 5000,
						'protocol': 'tcp'
					},
				],
				'hostname': 'amoltest',
				'user': 'amol',
				'privileged': True,
				'readonlyRootFilesystem': False,            
				
			},
		],
		volumes=[
			{
				'name': 'string',
				'host': {
					'sourcePath': 'string'
				}
			},
		],
		placementConstraints=[
			{
				'type': 'memberOf',
				'expression': 'string'
			},
		],
		requiresCompatibilities=[
			'EC2'|'FARGATE',
		],
		cpu='string',
		memory='string'
	)
    

if __name__ == '__main__':
    main()