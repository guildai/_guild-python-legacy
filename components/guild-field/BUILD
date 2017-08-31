#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-field",
    srcs = ["guild-field.html"],
    path = "/guild-field",
    deps = [
        "//components/guild-run:guild-run-data-listener",
        "//components/vz-field",
    ],
)
