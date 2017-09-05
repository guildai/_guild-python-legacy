package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-attrs",
    srcs = ["guild-attrs.html"],
    path = "/guild-attrs",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-run:guild-run-data-listener",
        "//components/vz-keyval-table",
    ],
)
