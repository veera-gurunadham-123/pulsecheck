# PulseCheck Ansible Capstone

## Overview
PulseCheck is a multi-tier application deployed using Ansible and Docker.

Components:
- Load Balancer (Nginx)
- Flask Application (app1, app2)
- PostgreSQL Database
- Ansible Automation
- Ansible Vault for secrets management

## Architecture

LB (Nginx)
|
+-- app1 (Flask)
|
+-- app2 (Flask)
|
+-- PostgreSQL

## Technologies Used

- Ansible
- Docker & Docker Compose
- Nginx
- Flask
- PostgreSQL
- Ansible Vault
- Ubuntu 24.04

## Deployment

Build containers:

```bash
docker compose up -d --build
```

Verify connectivity:

```bash
ansible all -m ping --vault-password-file .vault_pass.txt
```

Deploy stack:

```bash
ansible-playbook site.yml --vault-password-file .vault_pass.txt
```

## Smoke Test

```bash
ansible-playbook smoke_test.yml
```

## Verification

Application Health:

```bash
curl http://<APP_IP>:8000/health
```

Load Balancer:

```bash
curl http://<LB_IP>/
```
## Repository Structure

```text
.
├── inventory.ini
├── site.yml
├── smoke_test.yml
├── docker-compose.yml
├── Dockerfile.node
├── group_vars/
├── roles/
│   ├── postgres_db/
│   ├── python_app/
│   └── nginx_lb/
└── screenshots/
```

## Security

Secrets are stored using Ansible Vault.

Files excluded from Git:

- .vault_pass.txt
- pulsecheck_key
- pulsecheck_key.pub

