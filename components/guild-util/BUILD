package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-util",
    srcs = [
        "guild-util.html",
        "reduce.ts",
        "util.ts",
    ],
    path = "/guild-util",
    deps = [
        "//components/guild-imports:d3-time-format",
        "//components/guild-imports:numeraljs",
    ],
)
