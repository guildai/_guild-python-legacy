package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "vz-field",
    srcs = ["vz-field.html"],
    path = "/vz-field",
    deps = [
        "@org_polymer_paper_card",
        "@org_polymer_paper_styles",
        "@org_polymer_iron_icon",
    ],
)

ts_web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/vz-field",
    deps = [
        ":vz-field",
        "@org_polymer_webcomponentsjs",
        "@org_polymer_iron_demo_helpers",
        "//components/guild-icons",
    ]
)
