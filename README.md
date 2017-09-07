# Guild Python rewrite

This project intends to rewrite Guild AI in Python, replacing Erlang.

## Building

Guild Python requires Bazel 0.5.4 or higher to build. See [Installing
Bazel](https://docs.bazel.build/versions/master/install.html) for help
with you system.

Clone Guild Python from GitHub:

    $ git clone https://github.com/guildai/guild-python.git

Build Guild Python using the `bazel` command:

    $ cd guild-python
    $ bazel build guild

You may alternatively simply run `make`.

The initial Guild Python build will take some time as Bazel will
download serveral dependencies, including TensorBoard. Subsequent
builds will run faster.

If Guild Python builds successfully, run the `check` command with
tests:

    $ bazel-bin/guild/guild check --tests

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

***Guild Python is still a volatile project and features may suddenly
be added or break. We apologize for this instability and will work
aggressively to stabilize the project. In the meantime, we are
grateful for your patience! Please refer to [CHANGES.md](CHANGES.md)
for updates.***

### Commands

Below is a list of Guild Python commands and their status:

| Name     | Status                           |
| -------- | -------------------------------- |
| check    | working                          |
| evaluate | working                          |
| prepare  | working                          |
| project  | working                          |
| query    | working                          |
| runs     | working                          |
| train    | working                          |
| view     | active development, **BROKEN**   |

Several Guild Erlang commands have either been renamed or replaced by
new commands, or are not yet implemented in Guild Python. Refer to the
table below for details.

| Old command | New command     | Status          | Feature parity / notes  |
| ----------- | --------------- | --------------- | ----------------------- |
| check       | check           | implemented     | equivalent              |
| delete-eval | evals rm        | not implemented |                         |
| delete-run  | runs rm         | implemented     | enhanced (see run help) |
| evaluate    | evaluate        | implemented     | equivalent              |
| install     | install         | not implemented |                         |
| list-attrs  | query attrs     | not implemented | equivalent              |
| list-evals  | evals           | not implemented | enhanced                |
| list-models | project models  | implemented     | enhanced                |
| list-runs   | runs            | implemented     | equivalent              |
| package     | package         | not implemented |                         |
| prepare     | prepare         | implemented     | equivalent              |
| serve       | ???             | not impemented  | may be dropped          |
| status      | ???             | not impemented  | may be renamed/replaced |
| train       | train           | implemented     | equivalent              |
| uninstall   | uninstall       | not implemented |                         |
| view        | view            | active development, **BROKEN** |          |

### View

View is under active development. We're currently re-integrating with
TensorBoard, which is a significant refactor as TensorBoard has
changed quite a bit since our last integration:

- Stand alone project
- Use of Bazel for building and dependency management
- New plugin scheme that federates UI and backend logic
- Migration of TypeScript namespaces to ES6 modules

To simplify integration in the future, we're taking a big step in
Guild Python:

- Use Bazel for builds and dependency management
- Integrate TensorBoard directly into Guild Python as a dependency
- Use TensorBoard web dependencies (e.g. Polymer components, third
  party libraries, etc.) directly rather than duplicate them based on
  routine syncs

While this step is disruptive, it will control both our UI
dependencies and our use of TensorBoard. The result will be more
stable builds and UI behavior and easier synchronization with changes
made to TensorBoard.

### Python 3

Guild Python now supports Python 3. If there's a bug Guild Python that
occurs only under Python 3, we'll treat it with the same priority as a
bug occurring under Python 2.
