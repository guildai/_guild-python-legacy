package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-output",
    srcs = ["guild-output.html"],
    path = "/guild-output",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-datatable",
        "//components/guild-filter-input",
        "//components/guild-imports:d3-time-format",
        "//components/guild-run:guild-run-data-listener",
        "@org_polymer_paper_toolbar",
    ],
)
