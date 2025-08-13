# SudoSpawner

[![Latest PyPI version](https://img.shields.io/pypi/v/sudospawner?logo=pypi)](https://pypi.python.org/pypi/sudospawner)
[![Latest conda-forge version](https://img.shields.io/conda/vn/conda-forge/sudospawner?logo=conda-forge)](https://anaconda.org/conda-forge/sudospawner)
[![GitHub Workflow Status - Test](https://img.shields.io/github/actions/workflow/status/jupyterhub/sudospawner/test.yaml?logo=github&label=tests)](https://github.com/jupyterhub/sudospawner/actions)
[![Test coverage of code](https://codecov.io/gh/jupyterhub/sudospawner/branch/main/graph/badge.svg)](https://codecov.io/gh/jupyterhub/sudospawner)
[![Issue tracking - GitHub](https://img.shields.io/badge/issue_tracking-github-blue?logo=github)](https://github.com/jupyterhub/sudospawner/issues)
[![Help forum - Discourse](https://img.shields.io/badge/help_forum-discourse-blue?logo=discourse)](https://discourse.jupyter.org/c/jupyterhub)

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

2. [Add sudo access to the script](https://jupyterhub.readthedocs.io/en/stable/howto/configuration/config-sudo.html).

3. To configure JupyterHub to use SudoSpawner, add the following to your 
`jupyterhub_config.py`:

        c.JupyterHub.spawner_class = "sudo"
    
   The [JupyterHub documentation](http://jupyterhub.readthedocs.org/en/latest/index.html)
   has additional information about [creating a configuration file](https://jupyterhub.readthedocs.io/en/latest/getting-started/config-basics.html#generate-a-default-config-file),
   if needed, and recommended file locations for configuration files.

If you would like to use JupyterLab, then all you have to do is set the `default_url`
in `jupyterhub_config.py`:

    c.Spawner.default_url = '/lab'

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

The [Dockerfile](https://github.com/jupyter/sudospawner/blob/master/examples/Dockerfile) in this repo contains an example configuration for setting up a JupyterHub system, without any need to run anything as root.
