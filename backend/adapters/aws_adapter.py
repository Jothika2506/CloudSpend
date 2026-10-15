from .cloud_adapter import CloudAdapter
from moto import mock_aws
import boto3
import random

class AWSAdapter(CloudAdapter):
    """AWS-specific implementation using moto for local testing"""

    def __init__(self):
        self.region = "us-east-1"
        # Create instances once and reuse them
        self.instance_ids = self._create_mock_instances()

    def _create_mock_instances(self):
        """Create persistent mock EC2 instances"""
        with mock_aws():
            ec2 = boto3.client("ec2", region_name=self.region)
            # Create 2-4 instances
            num_instances = random.randint(2, 4)
            response = ec2.run_instances(ImageId="ami-12345678", MinCount=num_instances, MaxCount=num_instances)
            instance_ids = [inst['InstanceId'] for inst in response['Instances']]
            return instance_ids

    def get_instances(self):
        """Get all EC2 instances with metrics"""
        instances = []

        for instance_id in self.instance_ids:
            metrics = self.get_metrics(instance_id)
            instances.append({
                'instance_id': instance_id,
                'cloud_provider': self.get_cloud_name(),
                'state': 'running',
                'cpu': metrics['cpu'],
                'network': metrics['network'],
                'disk': metrics['disk']
            })

        return instances

    def get_metrics(self, instance_id):
        """Get CPU, Network, Disk metrics for an instance
        ~30% of instances are idle (low metrics), ~70% are active (high metrics)
        """
        # Decide if this instance should be idle or active
        is_idle = random.random() < 0.3

        if is_idle:
            # Idle metrics: all below thresholds
            cpu = round(random.uniform(1, 8), 1)           # Below 10%
            network = round(random.uniform(0.5, 4.5), 1)   # Below 5MB
            disk = round(random.uniform(0.1, 4.5), 1)      # Below 5MB
        else:
            # Active metrics: normal usage
            cpu = round(random.uniform(15, 95), 1)
            network = round(random.uniform(10, 99), 1)
            disk = round(random.uniform(10, 99), 1)

        return {
            'cpu': cpu,
            'network': network,
            'disk': disk
        }

    def stop_instance(self, instance_id):
        """Stop an EC2 instance"""
        # In production: use actual boto3
        # For mock: just log it
        return True