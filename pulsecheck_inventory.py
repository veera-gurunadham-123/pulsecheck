#!/usr/bin/env python3
"""
pulsecheck_inventory.py - dynamic inventory for the PulseCheck capstone.

Groups the containers by the "role" label set on each in docker-compose.yml
(lb, app, db), using `docker inspect`.

Usage:
    ansible-inventory -i pulsecheck_inventory.py --graph
    ansible all -i pulsecheck_inventory.py -m ping
"""
import json
import subprocess
import sys

NETWORK = "pulsecheck-net"


def get_containers():
    try:
        names = subprocess.check_output(
            ["docker", "ps", "--filter", "label=project=pulsecheck", "--format", "{{.Names}}"]
        ).decode().split()
    except subprocess.CalledProcessError as e:
        sys.exit(f"docker ps failed: {e}")

    containers = {}
    for name in names:
        raw = subprocess.check_output(["docker", "inspect", name])
        inspect = json.loads(raw)[0]
        networks = inspect["NetworkSettings"]["Networks"]
        if NETWORK not in networks:
            continue
        ip = networks[NETWORK]["IPAddress"]
        role = inspect["Config"]["Labels"].get("role", "unknown")
        containers[name] = {"ip": ip, "role": role}
    return containers


def build_inventory(containers):
    inventory = {
        "_meta": {"hostvars": {}},
        "all": {"children": []},
    }
    for name, info in containers.items():
        role = info["role"]
        if role not in inventory:
            inventory[role] = {"hosts": []}
            inventory["all"]["children"].append(role)
        inventory[role]["hosts"].append(name)
        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": info["ip"],
            "role": role,
        }
    return inventory


def main():
    containers = get_containers()
    inventory = build_inventory(containers)
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
