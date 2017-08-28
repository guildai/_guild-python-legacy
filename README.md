# Guild Python rewrite

This project intends to rewrite Guild AI in Python, replacing Erlang.

## Building

Guild Python requires Bazel 0.5.4 or higher to
build. See
[Installing Bazel](https://docs.bazel.build/versions/master/install.html) for
help with you system.

Clone Guild Python from GitHub:

    $ git clone https://github.com/guildai/guild-python.git

Build using Bazel:

    $ cd guild-python
    $ bazel build guild

You may alternatively simply run `make`.

The initial Guild Python build will take some time as Bazel will
download serveral dependencies, including TensorBoard. Subsequent
build should run much faster.

If Guild Python builds successfully, run the `check` command:

    $ bazel-bin/guild/guild check

Finally, run the test suite:

    $ bazel-bin/guild/guild check --all-tests

You may alternatively run `make check`.

Note that tests are now a part of the Guild Python binary and will be
available to run for end-users.

## Installing from a build

To run the `guild` command on your system, you may do one of the
following:

- Add `$GUILD_PYTHON_REPO/bazel-bin/guild` to your `PATH`
- Create a `guild` alias equal to `$GUILD_PYTHON_REPO/bazel-bin/guild/guild`

where `$GUILD_PYTHON_REPO` is the path to the cloned Guild Python
repository.

## What's working, what's not

***Guild Python is still a highly volatile project and features may
suddenly be added or break. We apologize for this instability and will
work aggressively to stabilize the project. In the meantime, we are
grateful for your patience! Please refer to [CHANGES.md](CHANGES.md)
for updates.***

### Commands

Below is a list of Guild Python commands and their status:

| Name     | Status                       |
| -------- | ---------------------------- |
| check    | working                      |
| evaluate | stub / not implemented       |
| prepare  | working                      |
| project  | working                      |
| query    | working                      |
| runs     | working                      |
| train    | working                      |
| view     | active development / broken) |

Several Guild Erlang commands have either been renamed or replaced by
new commands, or are not yet implemented in Guild Python. Refer to the
table below for details.

| Old command | New command     | Status / Notes      |
| ----------- | --------------- | ------------------- |
| check       | check           | equivalent |
| delete-eval | evals rm        | not implemented |
| delete-run  | runs rm         | enhanced |
| evaluate    | evaluate        | not implemented |
| install     | install         | not implemented |
| list-attrs  | query attrs     | not implemented |
| list-evals  | evals           | equivalent |
| list-models | project models  | enhanced |
| list-runs   | runs            | equivalent |
| package     | package         | not implemented |
| prepare     | prepare         | equivalent |
| serve       | ???             | not impemented, may be dropped |
| status      | ???             | not impemented, may be renamed or replaced |
| train       | train           | equivalent |
| uninstall   | uninstall       | not implemented |
| view        | view            | equivalent, active development, unstable |

### View

View is under active development. We're currently re-integrating with
TensorBoard, which is a significant refactor as TensorBoard has
changed quite a bit since our last integration:

- Stand alone project
- Use of Bazel for building and dependency management
- New plugin scheme that federates UI and backend logic

To simplify integration in the future, we're taking a big step in
Guild Python:

- Use Bazel for builds and dependency management
- Integrate TensorBoard directly into Guild Python as a dependency
- Use TensorBoard web dependencies (e.g. Polymer components, third
  party libraries, etc.) directly rather than duplicate them based on
  routine syncs

While this step is highly disruptive, it will strictly control both
our UI dependencies (thanks to Bazel's strict and fine-grained
dependency management facility) and our use of TensorBoard. The result
will be more stable builds and UI behavior and easier synchronization
with changes made to TensorBoard.

### Python 3

***Guild Python does not currently support Python 3.***

While earlier versions worked with Python 3, they suffered from some
problems:

- Third party dependencies had to be installed independently of Guild
  for Python 2 and Python 3
- As Python 3 is not the primary development platform, features would
  routinely break

As we are now including all of our dependencies in the build itself,
we are focussing on Python 2 and not supporting Python 3. Support for
Python 3, either a single distribution or a two separate
distributions, is planned, but we're working aggressively on these
priorities, in order:

- Stabilize the project to eliminate volatile and breaking changes
- Achieve feature parity with the Erlang version
- Complete support for `evaluate` and its related UI/visualizations
- Complete preliminary package support
