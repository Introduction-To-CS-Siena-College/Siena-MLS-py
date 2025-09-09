import requests
import warnings

import sys
from importlib import metadata # To enable getting MES version using __version__
class ManagementService: 
  
  def __init__(self):
    self.__version__ = metadata.version("Siena-MLS")

  def get_latest_version(self, package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()
    return data["info"]["version"]
    
  def get_installed_version(self, package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()
    return data["info"]["version"]

  def printVersion(self):
    print(f"Current MLS Version is ${self.__version}")
    print(sys.version)
    
  def getVersion(self):
    return self.__version__
    
  def notify_if_outdated(self):
    installed_version = self.__version__
    latest_version = self.get_latest_version("Siena-MLS")
    if latest_version > installed_version:
      warnings.warn(f"Friently Nudge: You are using {installed_version} of Siena-mls", DeprecationWarning)
