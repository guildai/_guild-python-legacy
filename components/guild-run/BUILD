package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-run",
    srcs = [
        "guild-run.html",
        "run.js",
    ],
    path = "/guild-run",
    deps = [
        "//components/guild-util",
    ],
)

web_library(
    name = "guild-run-data-listener",
    srcs = [
        "guild-run-data-listener.html",
    ],
    path = "/guild-run",
    deps = [
        "//components/guild-data:guild-data-listener",
    ],
)

web_library(
    name = "guild-run-compare-data-listener",
    srcs = [
        "guild-run-compare-data-listener.html",
    ],
    path = "/guild-run",
    deps = [
        "//components/guild-data:guild-data-listener",
    ],
)
