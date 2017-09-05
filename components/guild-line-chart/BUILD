package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-line-chart",
    srcs = ["guild-line-chart.html"],
    path = "/guild-line-chart",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/plugins/scalar/vz_line_chart",
    ],
)
