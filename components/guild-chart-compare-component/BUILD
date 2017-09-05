package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-chart-compare-component",
    srcs = ["guild-chart-compare-component.html"],
    path = "/guild-chart-compare-component",
    deps = [
        "//components/guild-chart-options",
        "//components/guild-compare-component-panel",
        "//components/guild-run:guild-run-compare-data-listener",
        "//components/guild-line-chart",
    ],
)
