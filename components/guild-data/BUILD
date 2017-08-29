#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-data",
    srcs = [
        "guild-data.html",
        "data.js",
    ],
    path = "/guild-data",
)

web_library(
    name = "guild-data-listener",
    srcs = ["guild-data-listener.html"],
    path = "/guild-data",
    deps = [
        ":guild-data",
        "//components/guild-util",
    ],
)
