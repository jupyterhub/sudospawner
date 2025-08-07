# Changes in sudospawner

## 0.5

### 0.5.2 - 2018-01-19

- Add `make_preexec_fn` method as an avenue for overriding pre-exec actions,
  e.g. setting resource limits. Default behavior is unchanged.

### 0.5.1 - 2017-10-11

- Fix bug preventing JupyterHub 0.8 from connecting to Spawners with default `ip`.

### 0.5.0 - 2017-09-26

- Remove deprecated code for supporting JupyterHub < 0.7.
  JupyterHub ≥ 0.7 is required.

## 0.4

### 0.4.1 - 2017-08-06

- Avoid invoking sudo for poll

### 0.4.0 - 2017-04-21

0.4 adds better error handling:

- report better errors when sudospawner fails; change unhelpful `ValueError: substring not found`
  message when parsing output fails to a more helpful message and log the unparsed data
- treat failures to signal the process as the process being missing, and log the failure, instead of raising errors

## 0.3

### 0.3.0 - 2016-10-10

- return ip, port from Spawner.start (future-compatibility, as setting ip, port directly is deprecated in JupyterHub 0.7)
- better handling of errors in the mediator
- allow overriding single-user spawn via sudospawner-singleuser script

## 0.2

### 0.2.0 - 2016-02-12

- Fixes for compatibility with jupyterhub-0.4
- Relay subprocess output to Hub, to reduce silent errors
- `sudospawner` executable **must** be in the same dir as `jupyterhub-singleuser`

## 0.1

### 0.1.0 - 2016-02-03

First release
