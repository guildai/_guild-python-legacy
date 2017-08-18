Runs
====

The 'guild.run' module provides support for representing runs.

>>> import guild.run

We'll use the sample runs directory for our data:

>>> runs_dir = sample("runs")

The function 'runs_for_runs_dir' will return a list of runs located in
the specified directory.

>>> runs = guild.run.runs_for_runs_dir(runs_dir)
>>> len(runs)
1

We can access run attrs directly:

>>> pprint(runs[0].attrs)
{'cmd': '...',
 'exit_status': '0',
 'model': 'intro',
 'started': '1502198513402',
 'stopped': '1502198513402'}

or by name:

>>> runs[0].attr("exit_status")
'0'
>>> runs[0].attr("model")
'intro'
>>> runs[0].attr("started")
'1502198513402'
