package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-fields",
    srcs = ["guild-fields.html"],
    path = "/guild-fields",
    deps = [
        "//components/guild-field",
        "//components/guild-styles",
    ],
)
