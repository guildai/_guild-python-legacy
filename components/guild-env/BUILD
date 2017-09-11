package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-env",
    srcs = [
        "guild-env.html",
        "env.ts",
    ],
    path = "/guild-env",
    deps = [
        "//components/guild-data:guild-data-listener",
    ],
)
