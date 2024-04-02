# Ansible Project: Server Hardening and Docker Registry Setup

This Ansible project automates the process of server hardening followed by setting up a private local Docker registry. The registry acts as a cache registry and facilitates obtaining Docker images for services like Nginx, MySQL, and WordPress.

## Requirements
- python3-pip Installed on controller node(s)
- Ansible installed on the controller node(s)
- Install [community.docker.docker_compose_v2 module](https://docs.ansible.com/ansible/latest/collections/community/docker/docker_compose_v2_module.html#ansible-collections-community-docker-docker-compose-v2-module)

## Usage

1. Ensure Ansible and Python3-pip are installed on your controller node(s).
2. Clone this repository on the controller node(s).
3. Put the Vault's password in [.secrets](.secrets) file
4. Set managed node(s) host and other configurations in the [hosts.yaml](inventory/hosts.yaml).

    **Note:** Ensure controller node can connect to the managed nodes using ssh

5. Run the Ansible playbook:

    ```bash
    ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -i inventory/hosts.yaml playbook.yaml
    ```

## What does this playbook do?

1. **Prepares the server:**
    - Installs common packages
    - Configures SSL certificates
    - Setups a proxy (to bypass sanctions and limitations)
    - Execute server hardening tasks to enhance server security.

2. **Runs a private Docker registry:**
    - Installs Docker and compose plugin (aka `docker-compose`)
    - Deploys a private local registry at reg.mahmoudisari.ir which serves as a cache registry, under reg.

3. **Deploys a WordPress site:**
    - Runs WordPress and MySQL on Docker
    - Configures nginx to server the website at wp.mahmoudisari.ir
