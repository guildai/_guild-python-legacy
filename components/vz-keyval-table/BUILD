package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")
load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")

ts_web_library(
    name = "vz-keyval-table",
    srcs = ["vz-keyval-table.html"],
    path = "/vz-keyval-table",
    deps = [
        "//components/guild-styles",
        "@org_polymer",
    ],
)

ts_web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/vz-keyval-table",
    deps = [
        ":vz-keyval-table",
        "@org_polymer_webcomponentsjs",
    ]
)

tensorboard_html_binary(
    name = "demo-bin",
    input_path = "/vz-keyval-table/demo.html",
    output_path = "/vz-keyval-table/demo-bin.html",
    deps = [":demo"],
)
