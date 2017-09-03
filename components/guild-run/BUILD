package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-run",
    srcs = [
        "guild-run.html",
        "run.ts",
    ],
    path = "/guild-run",
    deps = [
        "//components/guild-util",
    ],
)

ts_web_library(
    name = "guild-run-data-listener",
    srcs = [
        "guild-run-data-listener.html",
    ],
    path = "/guild-run",
    deps = [
        "//components/guild-run:guild-run",
        "//components/guild-data:guild-data-listener",
    ],
)

ts_web_library(
    name = "guild-run-compare-data-listener",
    srcs = [
        "guild-run-compare-data-listener.html",
    ],
    path = "/guild-run",
    deps = [
        "//components/guild-data:guild-data-listener",
    ],
)
