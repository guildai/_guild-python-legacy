package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")
load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")

ts_web_library(
    name = "guild-test",
    srcs = ["guild-test.html"],
    path = "/guild-test",
    deps = [
        "@org_polymer",
    ],
)

ts_web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/guild-test",
    deps = [
        ":guild-test",
    ]
)

tensorboard_html_binary(
    name = "demo-bin",
    input_path = "/guild-test/demo.html",
    output_path = "/guild-test/demo-bin.html",
    deps = [":demo"],
    _Vulcanize = "//java/org/guildai/vulcanize:Vulcanize",
)
