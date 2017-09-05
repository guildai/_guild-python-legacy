package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-compare-components",
    srcs = ["guild-compare-components.html"],
    path = "/guild-compare-components",
    deps = [
        ":guild-compare-component-select",
        "//components/guild-chart-compare-component",
        "//components/guild-keyval-compare-component",
        "//components/guild-styles",
    ],
)

ts_web_library(
    name = "guild-compare-component-select",
    srcs = ["guild-compare-component-select.html"],
    path = "/guild-compare-components",
    deps = [
        "//components/guild-data:guild-data-listener",
        "@org_polymer_iron_icons",
        "@org_polymer_iron_icon",
        "@org_polymer_paper_fab",
        "@org_polymer_paper_header_panel",
        "@org_polymer_paper_input",
        "@org_polymer_paper_item",
        "@org_polymer_paper_menu_button",
        "@org_polymer_paper_menu",
    ],
)
