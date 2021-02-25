import pulumi
import pulumi_aws as aws

#Define # of Swarm leader instances
no_of_leaders=1

#Define size of Swarm leader & worker instances
leader_size = 't3.small'

#SSH Key to provision
key_name = "aws-poc"
#read in leader data, to provision the instance
with open('init_script.swarm-leader.txt', 'r') as init_script:
    leader_user_data = init_script.read()
    print(leader_user_data)

#Prep AMI to use : aws ubuntu 20:https://cloud-images.ubuntu.com/locator/ec2/

ami = aws.get_ami(most_recent=True,
    filters=[
        aws.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
        ),
        aws.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"]) 

#Create leader nodes
for i in range(1,1+no_of_leaders):
    instance_name='swarm-leader'+str(i)
    server = aws.ec2.Instance(instance_name,
        instance_type=leader_size,
        vpc_security_group_ids=["sg-0263ccb5f77e20721"],
        user_data=leader_user_data,
        ami=ami.id,
        key_name=key_name)
    ip= 'leader_public_ip'+str(i)
    dns= 'leader_public_dns'+str(i)
    pulumi.export(ip, server.public_ip)
    pulumi.export(dns, server.public_dns)
