#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-run-status",
    srcs = ["guild-run-status.html"],
    path = "/guild-run-status",
    deps = [
        "//components/guild-run",
        "//components/guild-styles",
        "@org_guildai_fa_awesome",
    ],
)
