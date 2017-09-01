package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-flags",
    srcs = ["guild-flags.html"],
    path = "/guild-flags",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-run:guild-run-data-listener",
        "//components/vz-keyval-table",
    ],
)
