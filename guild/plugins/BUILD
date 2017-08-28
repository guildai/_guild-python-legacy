#-*-python-*-

package(default_visibility = ["//visibility:public"])

py_library(
    name = "plugins",
    srcs = ["__init__.py"],
    deps = [
        ":keras_plugin",
    ],
)

py_library(
    name = "keras_plugin",
    srcs = ["keras_plugin.py"],
    deps = [
        "//guild:log",
    ],
    data = [
        ":keras_run"
    ],
)

py_library(
    name = "keras_run",
    srcs = ["keras_run.py"],
    deps = [
        ":keras_placeholder"
    ],
)

py_library(
    # Placeholder for Keras dependency. We don't provide Keras and
    # instead rely on the user to install the desired version.
    name = "keras_placeholder",
)
