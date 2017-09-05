package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")
load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-field",
    srcs = ["guild-field.html"],
    path = "/guild-field",
    deps = [
        "//components/guild-run:guild-run-data-listener",
        "//components/vz-field",
    ],
)

ts_web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/guild-field",
    deps = [
        ":guild-field",
        "//components/guild-env",
        "//components/guild-view/demo:demo-data",
        "@org_polymer_webcomponentsjs",
        "@org_polymer_iron_demo_helpers",
        "@org_polymer_app_route",
    ]
)

tensorboard_html_binary(
    name = "demo-bin",
    input_path = "/guild-field/demo.html",
    output_path = "/guild-field/demo-bin.html",
    deps = [":demo"],
)
