package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-chart-options",
    srcs = ["guild-chart-options.html"],
    path = "/guild-chart-options",
    deps = [
        "//components/guild-component-options",
        "//components/guild-component-options:option-dropdown",
        "//components/guild-component-options:option-element",
        "//components/guild-smoothing-input",
        "@org_polymer_paper_item",
    ],
)
