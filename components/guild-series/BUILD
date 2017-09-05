package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-series",
    srcs = ["guild-series.html"],
    path = "/guild-series",
    deps = [
        "//components/guild-chart",
        "//components/guild-styles",
    ],
)
