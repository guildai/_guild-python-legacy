#-*-python-*-

package(default_visibility = ["//guild:visibility"])

py_library(
    name = "gpu_stats",
    srcs = ["gpu_stats.py"],
    deps = [
        "//guild:log",
        "//guild:task_support",
        "//guild:util",
    ],
)

py_library(
    name = "log_flags",
    srcs = ["log_flags.py"],
    deps = [
        "//guild:log",
    ],
)

py_library(
    name = "log_system_attrs",
    srcs = ["log_system_attrs.py"],
    deps = [
        "//guild:log",
        "//guild:system",
        "//guild:tensorflow_support",
    ],
)

py_library(
    name = "op_stats",
    srcs = ["op_stats.py"],
    deps = [
        "//guild:log",
        "//guild:task_support",
    ],
)

py_library(
    name = "snapshot_project",
    srcs = ["snapshot_project.py"],
    deps = [
        "//guild:app",
        "//guild:log",
        "//guild:opdir",
    ],
    data = [
        "//scripts:snapshot-project",
    ],
)

py_library(
    name = "sys_stats",
    srcs = ["sys_stats.py"],
    deps = [
        "//guild:log",
        "//guild:task_support",
    ],
)

py_library(
    name = "tensorflow_events",
    srcs = ["tensorflow_events.py"],
    deps = [
        "//guild:log",
        "//guild:task_support",
        # TODO TensorFlow/Board deps somehow
    ],
)
