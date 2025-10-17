# Changes in sudospawner

## 1.0

### 1.0.0 - 2025-10-17

1.0.0 fixes compatibility with Python >=3.13 and requires Python >=3.9.

([full changelog](https://github.com/jupyterhub/sudospawner/compare/0.5.2...1.0.0))

#### API and Breaking Changes

- Remove deprecated debug_mediator config (replaced by mediator_log_level) [#90](https://github.com/jupyterhub/sudospawner/pull/90) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Require jupyterhub 4+ and cleanup not required dependency on notebook [#86](https://github.com/jupyterhub/sudospawner/pull/86) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics), [@minrk](https://github.com/minrk))

#### Enhancements made

- Let c.JupyterHub.spawner_class be configurable with "sudo" [#94](https://github.com/jupyterhub/sudospawner/pull/94) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Replace debug_mediator with mediator_log_level [#54](https://github.com/jupyterhub/sudospawner/pull/54) ([@Siecje](https://github.com/Siecje), [@minrk](https://github.com/minrk))

#### Maintenance and upkeep improvements

- ci: fix declaring Python version [#99](https://github.com/jupyterhub/sudospawner/pull/99) ([@consideRatio](https://github.com/consideRatio))
- Add pre-commit hooks [#97](https://github.com/jupyterhub/sudospawner/pull/97) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- ci: run tests weekly to help flag issues over time [#93](https://github.com/jupyterhub/sudospawner/pull/93) ([@consideRatio](https://github.com/consideRatio))
- Add dependabot config to bump github actions [#91](https://github.com/jupyterhub/sudospawner/pull/91) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Transition from tornado's gen.coroutine to async/await [#89](https://github.com/jupyterhub/sudospawner/pull/89) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- Fix Dockerfile based example of using sudospawner [#88](https://github.com/jupyterhub/sudospawner/pull/88) ([@consideRatio](https://github.com/consideRatio))
- Expose **version** and version_info directly [#85](https://github.com/jupyterhub/sudospawner/pull/85) ([@consideRatio](https://github.com/consideRatio))
- Transition to pyproject.toml and modenize release docs/automation [#84](https://github.com/jupyterhub/sudospawner/pull/84) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics), [@minrk](https://github.com/minrk))
- Python 3.9-3.13 support with GitHub Actions fixes [#81](https://github.com/jupyterhub/sudospawner/pull/81) ([@ken-lauer](https://github.com/ken-lauer), [@consideRatio](https://github.com/consideRatio))
- Replace pipes with shlex [#80](https://github.com/jupyterhub/sudospawner/pull/80) ([@urlicht](https://github.com/urlicht), [@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))

#### Documentation improvements

- Fix broken link and rename examples folder to example [#98](https://github.com/jupyterhub/sudospawner/pull/98) ([@consideRatio](https://github.com/consideRatio))
- Refresh README for the 1.0.0 release [#96](https://github.com/jupyterhub/sudospawner/pull/96) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))
- docs: add dates to changelog entries [#83](https://github.com/jupyterhub/sudospawner/pull/83) ([@consideRatio](https://github.com/consideRatio))
- docs: fix broken badge and add typical badges [#82](https://github.com/jupyterhub/sudospawner/pull/82) ([@consideRatio](https://github.com/consideRatio))
- Fix URL for sudo configuration [#76](https://github.com/jupyterhub/sudospawner/pull/76) ([@pdebuyl](https://github.com/pdebuyl), [@consideRatio](https://github.com/consideRatio))
- Update running JupyterLab docs for SudoSpawner [#67](https://github.com/jupyterhub/sudospawner/pull/67) ([@kinow](https://github.com/kinow), [@consideRatio](https://github.com/consideRatio))
- Fix dead link to Dockerfile in README.md [#57](https://github.com/jupyterhub/sudospawner/pull/57) ([@lumbric](https://github.com/lumbric), [@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- Bump actions/setup-python from 5 to 6 [#101](https://github.com/jupyterhub/sudospawner/pull/101) ([@consideRatio](https://github.com/consideRatio))
- Bump actions/checkout from 4 to 5 [#92](https://github.com/jupyterhub/sudospawner/pull/92) ([@manics](https://github.com/manics))
- ci: add release workflow without pypa action [#69](https://github.com/jupyterhub/sudospawner/pull/69) ([@consideRatio](https://github.com/consideRatio), [@minrk](https://github.com/minrk))

#### Other merged PRs

- [pre-commit.ci] pre-commit autoupdate [#102](https://github.com/jupyterhub/sudospawner/pull/102) ([@consideRatio](https://github.com/consideRatio))
- Use GitHub Actions [#66](https://github.com/jupyterhub/sudospawner/pull/66) ([@kinow](https://github.com/kinow), [@minrk](https://github.com/minrk))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/sudospawner/graphs/contributors?from=2018-06-19&to=2025-10-17&type=c))

@consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3AconsideRatio+updated%3A2018-06-19..2025-10-17&type=Issues)) | @Frank-Steiner ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3AFrank-Steiner+updated%3A2018-06-19..2025-10-17&type=Issues)) | @ken-lauer ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Aken-lauer+updated%3A2018-06-19..2025-10-17&type=Issues)) | @kinow ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Akinow+updated%3A2018-06-19..2025-10-17&type=Issues)) | @lumbric ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Alumbric+updated%3A2018-06-19..2025-10-17&type=Issues)) | @mangecoeur ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Amangecoeur+updated%3A2018-06-19..2025-10-17&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Amanics+updated%3A2018-06-19..2025-10-17&type=Issues)) | @minrk ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Aminrk+updated%3A2018-06-19..2025-10-17&type=Issues)) | @pdebuyl ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Apdebuyl+updated%3A2018-06-19..2025-10-17&type=Issues)) | @Siecje ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3ASiecje+updated%3A2018-06-19..2025-10-17&type=Issues)) | @urlicht ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Aurlicht+updated%3A2018-06-19..2025-10-17&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fsudospawner+involves%3Ayuvipanda+updated%3A2018-06-19..2025-10-17&type=Issues))

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
