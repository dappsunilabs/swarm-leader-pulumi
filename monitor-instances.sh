#!/bin/bash
# script to monitor AWS instance meta data, get CPU, memory statistics
#on windows machine f executing linux, use this command ro remove carraige returns
#sed -i 's/\r$//' monitor-instances.sh
# to manipulate dates,
# date -d '+1 day' +"%Y-%m-%dT%H:%M:%SZ"
instances=$(aws ec2 describe-instances     --query 'Reservations[*].Instances[0].{Instance:InstanceId}')
i=$(echo "$instances" |jq -c '.[].Instance')
start_time=2021-02-10T23:18:00
end_time=2021-02-14T23:18:00
metric_name=CPUUtilization
for r in $i; do
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name $metric_name --dimensions Name=InstanceId,Value=$r --statistics Maximum --start-time $start_time --end-time $end_time --period 36000|jq -c ;
#aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name $metric_name --dimensions Name=InstanceId,Value=$r --statistics Maximum --start-time $start_time --end-time $end_time --period 36000|jq -c '.Datapoints[0] .Maximum';

#aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name $metric_name --dimensions Name=InstanceId,Value=$r --statistics Maximum --start-time $start_time --end-time $end_time --period 36000|jq -c '.Datapoints';

done
