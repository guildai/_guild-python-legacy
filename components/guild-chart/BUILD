package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-chart",
    srcs = ["guild-chart.html"],
    path = "/guild-chart",
    deps = [
        "//components/guild-chart-options",
        "//components/guild-component-panel",
        "//components/guild-line-chart",
        "//components/guild-run:guild-run-data-listener",
        "//components/guild-view:fullscreen-behavior",
        "@org_polymer_iron_icons",
        "@org_polymer_paper_icon_button",
    ],
)
