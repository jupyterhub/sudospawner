# SudoSpawner

## This is incomplete, and doesn't work yet

Enables [JupyterHub](https://github.com/jupyter/jupyterhub) to run without being root,
by running an adjacent local service as root that only spawns single-user servers.

The sudo spawner service cannot do anything other than start and poll single-user servers.
It listens on a local unix socket instead of tcp.

The only thing the Hub user needs sudo access for is starting the sudospawner service itself.

## setup

Start the service:

    python -m sudospawner.service

Tell JupyterHub to use SudoSpawner, by adding the following to your `jupyterhub_config.py`:

    c.JupyterHubApp.spawner_class='sudospawner.SudoSpawner'

