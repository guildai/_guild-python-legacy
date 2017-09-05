package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-data",
    srcs = [
        "guild-data.html",
        "data.ts",
    ],
    path = "/guild-data",
)

ts_web_library(
    name = "guild-data-listener",
    srcs = [
        "guild-data-listener.html",
        "data-listener.ts",
    ],
    path = "/guild-data",
    deps = [
        ":guild-data",
        "//components/guild-util",
    ],
)
