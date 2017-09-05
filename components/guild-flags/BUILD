package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-flags",
    srcs = ["guild-flags.html"],
    path = "/guild-flags",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-run:guild-run-data-listener",
        "//components/vz-keyval-table",
    ],
)
