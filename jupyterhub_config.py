# Configuration file for jupyterhub.

c = get_config()

# use the sudo spawner
c.JupyterHubApp.spawner_class = 'sudospawner.SudoSpawner'
