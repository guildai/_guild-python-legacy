# Changes

## September 6, 2017

- Remove `guild-lite`
- Support for Python 3
- Implement `evaluate` command

The alternative `guild-lite` build was a short-lived experiment. The
cost to carrying the view machinery is minor compared to the added
complexity to the build/release process.

Note that Guild View is still under active development. The `view`
command is disabled (though this can be overridden with a `--force`
flag).

Broken builds will be considered critical severity moving forward.

Bugs occuring under Python 3 will be fixed with the same priority as
Python 2.

## September 5, 2017

- Support for `guild-lite`

Guild View is not compiling due to heavy refactoring for ES6
support. View can be taken out of the CLI by building the
`guild:guild-lite` target.

## August 25, 2017

- Updated [README.md](README.md) with current project status.
