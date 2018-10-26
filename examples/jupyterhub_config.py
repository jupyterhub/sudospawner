# Configuration file for jupyterhub.

c = get_config()

# use the sudo spawner
c.JupyterHub.spawner_class = 'sudospawner.SudoSpawner'

c.SudoSpawner.mediator_log_level = "DEBUG"
c.JupyterHub.log_level = 10
