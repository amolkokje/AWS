import boto
import subprocess

mock_setup_port_dict = {
	'ec2': 5000,
	'ecs': 5001
}

def setup_server(service, port):
	cmd = 'moto_server {0} -p{1}'.format(service, port)
	print 'CMD = {0}'.format(cmd)
	return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	
mock_server_list = list()	
for server, port in mock_setup_port_dict.iteritems():
	mock_service = setup_server(server, port)
	#print 'PID = {0}'.format(mock_service.pid)  # this is not the right PID
	mock_server_list.append(mock_service)
	
	