package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "demo",
    srcs = ["index.html"],
    path = "/guild-view/demo",
    deps = [
        "//components/guild-view",
        "@org_polymer_webcomponentsjs",
        ":demo-data",

        "//components/vz-field",
    ],
)

ts_web_library(
    name = "demo-data",
    srcs = glob(["data/**"]),
    path = "/",
)
