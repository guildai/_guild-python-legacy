Guild View
==========

Guild View is primarily supported by two modules: `guild.view` and
`guild.view_http`. These tests focus on `guild.view`.

>>> import guild

The `view` module provides a `ProjectView` that is responsible for
formatting project state for Guild View. Let's first load a sample
project.

>>> project = guild.project.from_dir(sample("mnist"))

In addition to a project, a project view also provide 'settings' that
are specified by the user. These might include refresh intervals or
other values that are used by Guild View.

>>> settings = {
...     "refreshInterval": 5
... }

We can now create our project view:

>>> view = guild.view.ProjectView(project, settings)

For our tests, we need to make one change, which is to monkey patch
the location of the project runs. Our sample runs are located under
'samples/runs' and not under the sample project. Let's make that
change before calling any of the view methods.

>>> view._runs_dir = sample("runs")
>>> runs = view.runs()
>>> len(runs)
1

Formatted runs
--------------

We can use the `runs` method to return a list of formatted runs (each
represented by a dict, which can easily be converted to JSON):

>>> pprint(view.formatted_runs())
[{'cmd': '...',
  'dir': 'tests/samples/runs/2017-08-08T13-21-53Z-intro',
  'exit_status': 0,
  'extended_status': 'completed',
  'id': 2853895303,
  'model': 'intro',
  'started': 1502198513402,
  'status': 'stopped',
  'stopped': 1502198513402}]

Settings
--------

View settings are provided unmodified:

>>> view.settings()
{'refreshInterval': 5}

Flags
-----

Flags are provided on a per run basis. A run is specified by its run
ID:

>>> pprint(view.flags(runs[0].id))
[(u'epochs', u'1'),
 (u'datadir', u'./data'),
 (u'rundir', u'$RUNDIR'),
 (u'batch_size', u'100')]

We can alternatively use `None` to represent the latest run.

>>> pprint(view.flags(None))
[(u'epochs', u'1'),
 (u'datadir', u'./data'),
 (u'rundir', u'$RUNDIR'),
 (u'batch_size', u'100')]
