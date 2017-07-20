Project
=======

>>> import guild

Loading projects
----------------

Projects can be loaded from a file:

>>> p_from_file = guild.project.from_file(sample("guild.yml"))
>>> p_from_file.path
'tests/samples/guild.yml'

They can also be loaded from a directory, provided the project name is
'guild.yml':

>>> p_from_dir = guild.project.from_dir(samples_dir())
>>> p_from_dir.path
'tests/samples/guild.yml'

An IOError is raised if the project file doesn't exist:

>>> guild.project.from_file("does_not_exist")
Traceback (most recent call last):
IOError: [Errno 2] No such file or directory: 'does_not_exist'

We'll use the project reference `p` for the remaining tests.

>>> p = p_from_file

Project attributes
------------------

Project level attributes may be read using the `attr` method:

>>> p.attr("name")
'MNIST'
>>> p.attr("description")
'Guild MNIST example'
>>> p.attr("sources")
['*.py']
>>> p.attr("undefined") is None
True

Sections
--------

Project sections are grouped under section headings. You can return a
list of sections for a given heading using the `sections` method:

>>> [s.path for s in p.sections("models")]
[['models', 'expert'], ['models', 'intro']]

You can retrieve a section using `section`:

>>> s = p.section("models", "intro")
>>> s.path
['models', 'intro']

When a section key isn't available (e.g. the user doesn't specify it)
you can find a default section using `default_section`:

>>> s = p.default_section("models")
>>> s.path
['models', 'intro']
>>> s.attr("default")
True
