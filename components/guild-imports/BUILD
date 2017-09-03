package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:hacks.bzl", "tensorboard_typescript_bundle")
load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "d3-time-format",
    srcs = [
        "d3.d.ts",
        "d3-time-format.html",
        "@org_d3js_time_format//:d3-time-format.min.js",
    ],
    path = "/guild-imports",
)

ts_web_library(
    name = "numeraljs",
    srcs = [
        "@org_definitelytyped_types_numeral//:index.d.ts",
        "numeral.html",
        "@com_numeraljs//:numeral.js",
    ],
    path = "/guild-imports",
)

ts_web_library(
    name = "bootstrap-grid",
    srcs = [
        "bootstrap-grid.html",
        "@org_twbs_bootstrap//:css/bootstrap-grid.css",
    ],
    path = "/guild-imports",
    deps = [
        "//components/guild-bootstrap:grid-xxl",
    ],
)

ts_web_library(
    name = "datatables",
    srcs = [
        "datatables.html",
    ],
    path = "/guild-imports",
    deps = [
        ":jquery",
        "@net_datatables",
        "@net_datatables_dt",
    ],
)

ts_web_library(
    name = "jquery",
    srcs = [
        "jquery.html",
        "@com_jquery",
    ],
    path = "/guild-imports",
)

tensorboard_typescript_bundle(
    name = "d3_typings",
    out = "d3.d.ts",
    namespace_srcs = {
        "d3": [
            "@org_definitelytyped_types_d3_time_format//:index.d.ts",
        ],
    },
)
