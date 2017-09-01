package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-attrs",
    srcs = ["guild-attrs.html"],
    path = "/guild-attrs",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-run:guild-run-data-listener",
        "//components/vz-keyval-table",
    ],
)
