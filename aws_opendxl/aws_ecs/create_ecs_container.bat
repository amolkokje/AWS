setlocal

set TASKDEFJSON=C:\Users\aakokje\fargate-task-def.json
:: this name should be in the json file
set TASKDEFNAME=sample-amol-task-def 

set CLUSTERNAME=sample-amol-cluster
set SERVICENAME=sample-amol-service
set DESIREDTASKCOUNT=1

:: these should be available in your VPC
:: amol-sub-0
set SUBNET=subnet-89485aed
:: amol-sg
set SECURITYGROUP=sg-5a68ef10

aws ecs create-cluster --cluster-name %CLUSTERNAME%

aws ecs register-task-definition --cli-input-json file://%TASKDEFJSON%
aws ecs list-task-definitions

aws ecs create-service --cluster %CLUSTERNAME% --service-name %SERVICENAME% --task-definition %TASKDEFNAME% --desired-count %DESIREDTASKCOUNT% --launch-type "FARGATE" --network-configuration "awsvpcConfiguration={subnets=[%SUBNET%],securityGroups=[%SECURITYGROUP%]}"
aws ecs list-services --cluster %CLUSTERNAME%

aws ecs describe-services --cluster %CLUSTERNAME% --services %SERVICENAME%

endlocal