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

## Custom singleuser launch command


In order to limit what permissions the use of sudospawner grants the Hub,
when a single-user server is launched
the executable spawned is hardcoded as `dirname(sudospawner)/jupyterhub-singleuser`.
This requires the `sudospawner` executable to be in the same directory as the `jupyterhub-singleuser` command.
It is **very important** that users cannot modify the `bin/` directory containing `sudospawner`,
otherwise they can modify what `sudospawner` actually enables JupyterHub to do.

You may want to initialize user environment variables before launching the server, or do other initialization.
If you install a script called `sudospawner-singleuser` next to `sudospawner`,
this will be used instead of the direct `jupyterhub-singleuser` command.

For example, you might want to spawn notebook servers from conda environments that are revised and deployed separately from your hub instance. 

```bash
#!/bin/bash -l
set -e

# Activate the notebook environment
source /opt/miniconda/bin/activate /opt/envs/notebook-latest

# Show environment info in the log to aid debugging
conda info

# Delegate the notebook server launch to the jupyterhub-singleuser script.
# this is how most sudospawner-singleuser scripts should end.
exec "$(dirname "$0")/jupyterhub-singleuser" $@
```

## Example

The [Dockerfile](https://github.com/jupyter/sudospawner/blob/master/Dockerfile) in this repo contains an example configuration for setting up a JupyterHub system, without any need to run anything as root.
