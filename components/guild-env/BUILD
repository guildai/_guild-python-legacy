#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-env",
    srcs = [
        "guild-env.html",
    ],
    path = "/guild-env",
    deps = [
        "//components/guild-data:guild-data-listener",
    ],
)
