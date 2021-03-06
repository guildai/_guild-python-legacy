Project Util
============

The module `guild.project_util` provides a variety of utility
functions related to projects.

>>> import guild.project
>>> import guild.project_util

Resolving extends
-----------------

The function `resolve_extends` will merge attributes defined in a
*template* into items that reference that template in their `extends`
attribute. Any item in a project may be a template and referenced
using a path consisting of the keys or indexes starting from the
project root and ending with the item itself. Path parts are separeted
with a forward slash ("/"). If the item is a member of a dict, it's
key in the dict is used. If the item is a member of a list, its
zero-based index is used. An item may additionally define an `id`
attribute, which may also be used to identify it. As a shortcut, an
item's key may be used directly without specifying the full path. In
cases where the same key or id attribute is defined for multiple
items, the referenced item is non-deterministically selected. In such
cases, the user must use the item's full path.

Only dict items are indexed. Lists, scalars and string values cannot
be referenced using this scheme.

Indexing examples
.................

To illustrate the template reference scheme, we'll work with
`_project_templates`, which returns a map (dict) of item keys to their
corresponding items. The following function will generate a templates
map from a project string:

>>> def templates_from_string(s):
...     project = guild.project.from_string(p_str)
...     return guild.project_util._project_templates(project)

Let's first consider a simple project with a single item with two
attributes:

>>> p_str = """
... item:
...   attr1: 1
...   attr2: 2
... """

The project template generated from this looks like this:

>>> templates = templates_from_string(p_str)
>>> pprint(templates)
{'item': {'attr1': 1, 'attr2': 2}}

Note that the two scalar values ("item/attr1" and "item/attr2") are no
indexed.

Next, let's consider a project with a single list item containing two
child items:

>>> p_str = """
... item:
...   - attr1: 1
...   - attr2: 2
... """

>>> templates = templates_from_string(p_str)
>>> pprint(templates)
{'0': {'attr1': 1},
 '1': {'attr2': 2},
 'item/0': {'attr1': 1},
 'item/1': {'attr2': 2}}

Note that indexed items are references:

>>> templates["0"] == templates["item/0"]
True

In the next example, the project contains items that define 'id'
attributes, which are also used in the indexing scheme.

>>> p_str = """
... item1:
...   item2:
...      id: item2_alias
...      attr12: 12
...   item3:
...     - id: item4
...       attr14: 14
...     - id: item5
...       attr15: 15
... """

>>> templates = templates_from_string(p_str)
>>> pprint(templates)
{'0': {'attr14': 14, 'id': 'item4'},
 '1': {'attr15': 15, 'id': 'item5'},
 'item1': {'item2': {'attr12': 12, 'id': 'item2_alias'},
           'item3': [{'attr14': 14, 'id': 'item4'},
                     {'attr15': 15, 'id': 'item5'}]},
 'item1/item2': {'attr12': 12, 'id': 'item2_alias'},
 'item1/item2_alias': {'attr12': 12, 'id': 'item2_alias'},
 'item1/item3/0': {'attr14': 14, 'id': 'item4'},
 'item1/item3/1': {'attr15': 15, 'id': 'item5'},
 'item1/item3/item4': {'attr14': 14, 'id': 'item4'},
 'item1/item3/item5': {'attr15': 15, 'id': 'item5'},
 'item2': {'attr12': 12, 'id': 'item2_alias'},
 'item2_alias': {'attr12': 12, 'id': 'item2_alias'},
 'item4': {'attr14': 14, 'id': 'item4'},
 'item5': {'attr15': 15, 'id': 'item5'}}

Resolve examples
................

As described above, items containing an 'extends' attribute may
reference dict items using either their full key path or their key
itself (provided the key is unique in the project).

Let's define a function that helps us resolve a project from a string
definition.

>>> def resolve_from_string(s):
...     project = guild.project.from_string(p_str)
...     return guild.project_util.resolve_extends(project)

Our first example is a simple case where one item extends another
without adding or redefining attributes:

>>> p_str = """
... item1:
...   attr1: 1
... item2:
...   extends: item1
... """

The resolved project looks lke this:

>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': 1}, 'item2': {'attr1': 1}}

Extending items (i.e. items that define an 'extends' attribute) may
add new attributes:

>>> p_str = """
... item1:
...   attr1: 1
... item2:
...   extends: item1
...   attr2: 2
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': 1}, 'item2': {'attr1': 1, 'attr2': 2}}

They may also redefine attributes:

>>> p_str = """
... item1:
...   attr1: 1
...   attr2: 2
... item2:
...   extends: item1
...   attr1: 1.2
...   attr3: 3
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': 1, 'attr2': 2},
 'item2': {'attr1': 1.2, 'attr2': 2, 'attr3': 3}}

Extends may be used by list items:

>>> p_str = """
... item1:
...   attr1: 1
...   attr2: 2
... item2:
...   - extends: item1
...     attr1: 1.2
...     attr3: 3
...   - extends: item1
...     attr2: 2.2
...     attr4: 4
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': 1, 'attr2': 2},
 'item2': [{'attr1': 1.2, 'attr2': 2, 'attr3': 3},
           {'attr1': 1, 'attr2': 2.2, 'attr4': 4}]}

Extends applies to extended items -- i.e. extends supports multiple
levels:

>>> p_str = """
... item1:
...   attr1: 1
...   attr2: 2
... item2:
...   extends: item1
...   attr2: 2.2
...   attr3: 3
... item3:
...   extends: item2
...   attr2: 3.2
...   attr4: 4
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': 1, 'attr2': 2},
 'item2': {'attr1': 1, 'attr2': 2.2, 'attr3': 3},
 'item3': {'attr1': 1, 'attr2': 3.2, 'attr3': 3, 'attr4': 4}}

Cycles are supported, however attribute redefinition is
non-deterministic.

>>> p_str = """
... item1:
...   extends: item2
...   attr1: 1.1
...   attr2: 2
... item2:
...   extends: item1
...   attr1: 2.1
...   attr3: 3
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': ..., 'attr2': 2, 'attr3': 3},
 'item2': {'attr1': ..., 'attr2': 2, 'attr3': 3}}

Here's an example that uses full item paths.

>>> p_str = """
... item1:
...   item2:
...     attr1: 1
...     attr2: 2
... item3:
...   extends: item1/item2
...   attr2: 2.1
...   attr3: 3
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'item2': {'attr1': 1, 'attr2': 2}},
 'item3': {'attr1': 1, 'attr2': 2.1, 'attr3': 3}}

If an extended item is empty or doesn't exist, the extending item is
not modified:

>>> p_str = """
... item1:
...   extends: doesnt_exist
...   attr1: 1
...   attr2: 2
... """
>>> resolved = resolve_from_string(p_str)
>>> pprint(resolved.data)
{'item1': {'attr1': 1, 'attr2': 2}}

Project includes
----------------

Guild provides projects with base information via the
`include/project-base.yml`. This file contains default definitions for
views, components, and templates. `project-base.yml` is applied to a
user's project as a *resolve* step in Guild View. User projects may
redefine included values, either by adding or modifying their
attributes or by replacing values entirely.

You can see the effect of the resolve step by running the following
command from the CLI:

    guild project --resolve

This will print the current project (or the project referenced via
-P/--project) in YAML format. This is useful for debugging the resolve
step.

The function `guild.project_util.apply_project_include` is used to
apply an include to a project.

Let's creat a helper function to apply an include and print the
resulting project data:

>>> def apply_include(include, target):
...     applied = guild.project_util.apply_project_include(include, target)
...     pprint(applied.data)

Next we'll create a simple include project:

>>> include_project = guild.project.from_string("""
... foo:
...   attr1: 1
...   attr2: 2
... bar:
...   attr3: 3
...   attr4: [4.1, 4.2]
... """)

Next we'll define a project that replaced 'foo' and modifies 'bar':

>>> user_project = guild.project.from_string("""
... foo:
...   attr1: 1.1
...   attr2: 2.1
...   attr3: 3.1
... bar+:
...   attr3: 3.1
...   attr5: 5
... """)

Note that 'bar' is defined using a '+' suffix. This indicates that the
section should be merged into any included 'bar' section.

When we apply the include to the user project, we see that user 'bar'
is merged into the include 'bar':

>>> apply_include(include_project, user_project)
{'bar': {'attr3': 3.1, 'attr4': [4.1, 4.2], 'attr5': 5},
 'foo': {'attr1': 1.1, 'attr2': 2.1, 'attr3': 3.1}}

New sections are always added:

>>> user_project_2 = guild.project.from_string("""
... baz:
...   attr5: 5
...   attr6: 6
... """)
>>> apply_include(include_project, user_project_2)
{'bar': {'attr3': 3, 'attr4': [4.1, 4.2]},
 'baz': {'attr5': 5, 'attr6': 6},
 'foo': {'attr1': 1, 'attr2': 2}}

Attempting to merge a non-existing section is equivalent to adding it:

>>> user_project_3 = guild.project.from_string("""
... baz+:
...   attr5: 5
...   attr6: 6
... """)
>>> apply_include(include_project, user_project_3)
{'bar': {'attr3': 3, 'attr4': [4.1, 4.2]},
 'baz': {'attr5': 5, 'attr6': 6},
 'foo': {'attr1': 1, 'attr2': 2}}

Lists can be replaced:

>>> user_project_4 = guild.project.from_string("""
... bar+:
...   attr4: [4.3, 4.4]
... """)
>>> apply_include(include_project, user_project_4)
{'bar': {'attr3': 3, 'attr4': [4.3, 4.4]}, 'foo': {'attr1': 1, 'attr2': 2}}

Lists can also be merged, which appends the new values:

>>> user_project_5 = guild.project.from_string("""
... bar+:
...   attr4+: [4.3, 4.4]
... """)
>>> apply_include(include_project, user_project_5)
{'bar': {'attr3': 3, 'attr4': [4.1, 4.2, 4.3, 4.4]},
 'foo': {'attr1': 1, 'attr2': 2}}

To append to a section, the section content must be of the same
type. Type mismatches are silently ignored.

>>> user_project_6 = guild.project.from_string("""
... bar+: 6
... """)
>>> apply_include(include_project, user_project_6)
{'bar': {'attr3': 3, 'attr4': [4.1, 4.2]}, 'foo': {'attr1': 1, 'attr2': 2}}

>>> user_project_7 = guild.project.from_string("""
... bar+: [1, 2]
... """)
>>> apply_include(include_project, user_project_7)
{'bar': {'attr3': 3, 'attr4': [4.1, 4.2]}, 'foo': {'attr1': 1, 'attr2': 2}}

However, sections may be redefined using different types:

>>> user_project_7 = guild.project.from_string("""
... bar: 6
... """)
>>> apply_include(include_project, user_project_7)
{'bar': 6, 'foo': {'attr1': 1, 'attr2': 2}}
