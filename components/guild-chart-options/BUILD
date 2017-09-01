package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
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
