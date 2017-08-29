#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "d3",
    srcs = [
        "d3.html",
        "@org_d3js//:d3.min.js",
    ],
    path = "/guild-imports",
)

web_library(
    name = "numeraljs",
    srcs = [
        "numeral.html",
        "@com_numeraljs//:numeral.js",
    ],
    path = "/guild-imports",
)
