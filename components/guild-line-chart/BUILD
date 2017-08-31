#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-line-chart",
    srcs = ["guild-line-chart.html"],
    path = "/guild-line-chart",
    deps = [
        "@org_tensorflow_tensorboard//tensorboard/plugins/scalar/vz_line_chart",
    ],
)
