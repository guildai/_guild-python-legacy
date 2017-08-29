#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "d3-time-format",
    srcs = [
        "d3-time-format.html",
        "@org_d3js_time_format//:d3-time-format.min.js",
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
