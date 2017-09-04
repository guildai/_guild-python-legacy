package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:hacks.bzl", "tensorboard_typescript_bundle")
load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "d3-time-format",
    srcs = [
        "d3.d.ts",
        "@org_d3js_time_format//:d3-time-format.min.js",
        "d3-time-format.html",
    ],
    path = "/guild-imports",
)

tensorboard_typescript_bundle(
    name = "d3_typings",
    out = "d3.d.ts",
    namespace_srcs = {
        "d3": [
            "@org_definitelytyped_d3_time_format//:index.d.ts",
        ],
    },
)

ts_web_library(
    name = "numeraljs",
    srcs = [
        "numeral.d.ts",
        "@com_numeraljs//:numeral.js",
        "numeral.html",
    ],
    path = "/guild-imports",
)

genrule(
    name = "numeral_typings",
    srcs = ["@org_definitelytyped_numeral//:index.d.ts"],
    outs = ["numeral.d.ts"],
    cmd = "cp $< $@"
)

ts_web_library(
    name = "bootstrap-grid",
    srcs = [
        "@org_twbs_bootstrap//:css/bootstrap-grid.css",
        "bootstrap-grid.html",
    ],
    path = "/guild-imports",
    deps = [
        "//components/guild-bootstrap:grid-xxl",
    ],
)

ts_web_library(
    name = "datatables",
    srcs = [
        "datatables.d.ts",
        "datatables.html",
    ],
    path = "/guild-imports",
    deps = [
        ":jquery",
        "@net_datatables",
        "@net_datatables_dt",
    ],
)

genrule(
    name = "datatable_typings",
    srcs = ["@org_definitelytyped_datatables//:index.d.ts"],
    outs = ["datatables.d.ts"],
    cmd = "cp $< $@"
)

ts_web_library(
    name = "jquery",
    srcs = [
        "jquery.d.ts",
        "@com_jquery",
        "jquery.html",
    ],
    path = "/guild-imports",
)

genrule(
    name = "jquery_typings",
    srcs = ["@org_definitelytyped_jquery//:index.d.ts"],
    outs = ["jquery.d.ts"],
    cmd = "cp $< $@"
)
