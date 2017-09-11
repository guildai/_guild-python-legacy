package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-compare-component-panel",
    srcs = ["guild-compare-component-panel.html"],
    path = "/guild-compare-component-panel",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-view:fullscreen-behavior",
        "@org_polymer_iron_icons",
        "@org_polymer_paper_icon_button",
    ],
)
