from .cloud_adapter import CloudAdapter
import random

class AzureAdapter(CloudAdapter):
    """Azure-specific implementation using mock for local testing"""

    def __init__(self):
        self.subscription_id = "mock-subscription-id"
        self.resource_group = "mock-resource-group"
        # Persistent instance list (same across scans)
        self.mock_instances = [
            'azure-vm-01',
            'azure-vm-02',
            'azure-vm-03',
        ]

    def get_instances(self):
        """Get all Azure VM instances with metrics"""
        instances = []

        for vm_name in self.mock_instances:
            metrics = self.get_metrics(vm_name)
            instances.append({
                'instance_id': vm_name,
                'cloud_provider': self.get_cloud_name(),
                'state': 'VM running',
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
        """Stop an Azure VM instance"""
        # In production: use Azure SDK
        return True