package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-keyval-compare-component",
    srcs = ["guild-keyval-compare-component.html"],
    path = "/guild-keyval-compare-component",
    deps = [
        "//components/guild-compare-component-panel",
        "//components/guild-run:guild-run-compare-data-listener",
        "//components/guild-run-dropdown-menu",
        "//components/guild-styles",
        "//components/guild-imports:jsondiffpatch",
        "@org_polymer_iron_collapse",
        "@org_polymer_paper_toggle_button",
    ],
)
