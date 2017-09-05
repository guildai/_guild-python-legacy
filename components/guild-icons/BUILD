package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-icons",
    srcs = ["guild-icons.html"],
    path = "/guild-icons",
    deps = [
        "@org_polymer_iron_icons",
        "@org_pkaske_font_awesome_polymer_icons",
    ],
)
