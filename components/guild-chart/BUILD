package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-chart",
    srcs = ["guild-chart.html"],
    path = "/guild-chart",
    deps = [
        "//components/guild-chart-options",
        "//components/guild-component-panel",
        "//components/guild-line-chart",
        "//components/guild-run:guild-run-data-listener",
        "//components/guild-view:guild-fullscreen-behavior",
        "@org_polymer_iron_icons",
        "@org_polymer_paper_icon_button",
    ],
)
