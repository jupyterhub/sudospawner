# Configuration file for jupyterhub
c = get_config()

c.JupyterHub.spawner_class = "sudo"
c.Authenticator.allow_all = True

c.SudoSpawner.mediator_log_level = "DEBUG"
c.JupyterHub.log_level = "DEBUG"
