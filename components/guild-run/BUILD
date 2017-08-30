#-*-python-*-

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
