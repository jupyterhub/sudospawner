# Configuration file for jupyterhub.

c = get_config()

# use the sudo spawner
c.JupyterHub.spawner_class = 'sudospawner.SudoSpawner'

c.SudoSpawner.debug_mediator = True
c.JupyterHub.log_level = 10
