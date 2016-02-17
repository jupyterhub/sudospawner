# SudoSpawner

The SudoSpawner enables [JupyterHub](https://github.com/jupyter/jupyterhub)
to spawn single-user servers without being root, by spawning an intermediate
process via `sudo`, which takes actions on behalf of the user.

The ``sudospawner`` mediator, the intermediate process, can only do two things:

1. send a signal to another process using the os.kill() call
2. spawn single-user servers

Launching the ``sudospawner`` script is the only action that requires a
JupyterHub administrator to have ``sudo`` access to execute.

## Installation and setup

1. Install:

        pip install -e .

2. [Add sudo access to the script](https://github.com/jupyter/jupyterhub/wiki/Using-sudo-to-run-JupyterHub-without-root-privileges).

3. To configure JupyterHub to use SudoSpawner, add the following to your 
`jupyterhub_config.py`:

        c.JupyterHub.spawner_class='sudospawner.SudoSpawner'
    
   The [JupyterHub documentation](http://jupyterhub.readthedocs.org/en/latest/index.html)
   has additional information about [creating a configuration file](http://jupyterhub.readthedocs.org/en/latest/getting-started.html#how-to-configure-jupyterhub),
   if needed, and [recommended file locations for configuration files](http://jupyterhub.readthedocs.org/en/latest/getting-started.html#file-locations).

## Example

The [Dockerfile](https://github.com/jupyter/sudospawner/blob/master/Dockerfile) in this repo contains an example configuration for setting up a JupyterHub system,
without any need to run anything as root.
