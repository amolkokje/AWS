import os
import boto3
from moto import mock_s3, mock_ecs, mock_ec2, mock_cloudformation


# Broker/
# SNS triggers Lambda
# Lambda has DXL client which connects to the broker and sends event /dxl/test/event

vpc_name = 'test_vpc'
subnet_name = 'test_subnet'
cluster_name = 'test_cluster'
service_name = 'test_service'
task_def_family_name = 'test_task_family'
task_def_name = 'test_task_def'
task_name = 'test_task'
container_name = 'test_container'
image_name = 'amolkokje/opendxl-environment-centos'
    
@mock_s3
@mock_ec2
@mock_ecs
@mock_cloudformation
def main():
    s3_client = boto3.client('s3')
    ec2_client = boto3.client('ec2')
    ecs_client = boto3.client('ecs')
    #vpc_id, subnet_id = deploy_vpc_subnet(ec2_client)
    #print "VPC={}, SUBNET={}".format(vpc_id, subnet_id)
    #deploy_dxlbroker(ecs_client, vpc_id, subnet_id)
    deploy_dxlbroker(ec2_client, ecs_client)


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
    
"""    
def deploy_dxlbrokerb(client, vpc_id, subnet_id):
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
	
"""    

def deploy_dxlbroker(ec2_client, ecs_client):
    print "CREATE CLUSTER"
    response = ecs_client.create_cluster(
        clusterName=cluster_name
    )
    print response

    print '#############################################################################'
    print "RUN INSTANCE"
    response = ec2_client.run_instances(
        ImageId="ami-a98cb2c3",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        IamInstanceProfile={
            "Name": "ecsInstanceRole"
        },
        UserData="#!/bin/bash \n echo ECS_CLUSTER=" + cluster_name + " >> /etc/ecs/ecs.config"
    )
    print response

    print '#############################################################################'
    print 'REGISTER TASK DEFINITION'
    response = ecs_client.register_task_definition(
        containerDefinitions=[
            {
              "name": container_name,
              "image": image_name,
              "essential": True,
              "portMappings": [
                {
                  "containerPort": 80,
                  "hostPort": 80
                }
              ],
              "memory": 300,
              "cpu": 10
            }
        ],
        family=task_def_name
    )
    print response

    print '#############################################################################'
    print 'CREATE SERVICE'
    response = ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_def_name,
        desiredCount=1,
        clientToken='request_identifier_string',
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 50
        }
    )
    print response
    
    
if __name__ == '__main__':
    main()