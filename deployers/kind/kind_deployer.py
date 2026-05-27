import os
import subprocess
from typing import Dict, Any
from deployers.base import Deployer

class KinDDeployer(Deployer):
    """
    KinD implementation of the Deployer interface.
    """
    def __init__(self, cluster_name: str = "devops-bench-kind", **config):
        self.cluster_name = cluster_name
        self.config = config

    def up(self) -> None:
        # Check if cluster already exists
        check_cmd = ["kind", "get", "clusters"]
        print(f"Checking existing KinD clusters: {' '.join(check_cmd)}")
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and self.cluster_name in result.stdout.splitlines():
            print(f"KinD cluster {self.cluster_name} already exists. Loading kubeconfig.")
            # Setup kubeconfig context
            subprocess.run(["kind", "export", "kubeconfig", "--name", self.cluster_name], check=True)
        else:
            print(f"KinD cluster {self.cluster_name} does not exist. Creating it.")
            cmd = ["kind", "create", "cluster", "--name", self.cluster_name]
            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)

    def down(self) -> None:
        print(f"Tearing down KinD cluster {self.cluster_name}...")
        cmd = ["kind", "delete", "cluster", "--name", self.cluster_name]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

    def get_cluster_info(self) -> Dict[str, Any]:
        kubeconfig_path = os.path.expanduser("~/.kube/config")
        return {
            "name": self.cluster_name,
            "zone": "local",
            "project": "local-kind",
            "kubeconfig_path": kubeconfig_path
        }
