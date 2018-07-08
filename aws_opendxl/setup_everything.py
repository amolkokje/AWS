import os
import boto3
from moto import mock_s3, mock_ecs, mock_ec2, mock_cloudformation


# Broker/
# SNS triggers Lambda
# Lambda has DXL client which connects to the broker and sends event /dxl/test/event

vpc_name = 'test_vpc'
subnet_name = 'test_subnet'
cluster_name = 'test_cluster'
task_def_name = 'test_task_def'
task_name = 'test_task'
container_name = 'test_container'
    
@mock_s3
@mock_ec2
@mock_ecs
@mock_cloudformation
def main():
    s3_client = boto3.client('s3')
    ec2_client = boto3.client('ec2')
    ecs_client = boto3.client('ecs')
    vpc_id, subnet_id = deploy_vpc_subnet(ec2_client)
    print "VPC={}, SUBNET={}".format(vpc_id, subnet_id)
    deploy_dxlbroker(ecs_client, vpc_id, subnet_id)


def deploy_vpc_subnet(client):
    vpc = client.create_vpc(
		CidrBlock='10.0.0.0/8',
		AmazonProvidedIpv6CidrBlock=False,
		InstanceTenancy='default'
	)	
    print "VPC = {}".format(vpc)
    vpc_id = vpc['Vpc']['VpcId']
    subnet = client.create_subnet(CidrBlock='10.0.0.0/16', VpcId=vpc_id)
    print "Subnet = {}".format(subnet)
    subnet_id = subnet['Subnet']['SubnetId']
    return vpc_id, subnet_id
    
    
def deploy_dxlbroker(client, vpc_id, subnet_id):
    print 'Deploying dxlbroker container ...'
    client.create_cluster(clusterName=cluster_name)
    task_def = client.register_task_definition( 
        family=task_def_name,
        containerDefinitions=[
			{
                'name': container_name,
                'image': 'amolkokje/opendxl-environment-centos',
                'portMappings': [
                    {
                        'containerPort': 8000,
                        'hostPort': 5000,
                        'protocol': 'tcp'
                    },
                ],
                #'hostname': 'amoltest',
                'user': 'amol',
                'privileged': True,
                'readonlyRootFilesystem': False
            }   
        ],
        requiresCompatibilities=[
            'FARGATE'
        ]
    )
    print "Task Definition = {}".format(task_def)
    print "Task definitions = {}".format(client.list_task_definitions())
	
    """
    response = client.run_task(
		cluster=cluster_name,
		taskDefinition='{}:1'.format(task_def_name),
		count=1,
		launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    subnet_id
                ]
            }
        }
    )
    print "Response = {}".format(response)	
    print "Tasks = {}".format(client.list_tasks())
	"""
    
    print "Deploying dxlbroker done."
	

if __name__ == '__main__':
    main()