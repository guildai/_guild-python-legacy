#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-util",
    srcs = [
        "guild-util.html",
        "reduce.js",
        "util.js",
    ],
    path = "/guild-util",
    deps = [
        "//components/guild-imports:d3",
        "//components/guild-imports:numeraljs",
    ],
)
