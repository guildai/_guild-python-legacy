Package sources
===============

>>> import guild.source

>>> mnist = guild.source.Pkg(sample("packages/mnist.yml"))
>>> mnist.name
'mnist'
>>> mnist.version
'0.1.0'
>>> mnist.tags
['example', 'tutorial', 'mnist']

Comparing versions
------------------

The `guild.source.compare_versions` function can be used to compare
two version strings. If the strings can be parsed as semantic
versioned strings, the rules governing semantic versions are used to
compare the values.

>>> guild.source.compare_versions("1.0.2", "1.0.11")
-1

Versions that cannot be parsed as semantic versions are compared as
strings:

>>> guild.source.compare_versions("1.2", "1.11")
1
