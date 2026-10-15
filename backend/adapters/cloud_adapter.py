from abc import ABC, abstractmethod

class CloudAdapter(ABC):
    """Base class for cloud-specific implementations"""
    
    @abstractmethod
    def get_instances(self):
        """Get all instances from the cloud provider"""
        pass
    
    @abstractmethod
    def get_metrics(self, instance_id):
        """Get CPU, Network, Disk metrics for an instance"""
        pass
    
    @abstractmethod
    def stop_instance(self, instance_id):
        """Stop an instance"""
        pass
    
    def get_cloud_name(self):
        """Return the cloud provider name"""
        return self.__class__.__name__.replace('Adapter', '')