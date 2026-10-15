# C:\Projects-and-works\CloudSpend\backend\adapters\__init__.py

from .cloud_adapter import CloudAdapter
from .aws_adapter import AWSAdapter
from .gcp_adapter import GCPAdapter
from .azure_adapter import AzureAdapter

__all__ = ['CloudAdapter', 'AWSAdapter', 'GCPAdapter', 'AzureAdapter']