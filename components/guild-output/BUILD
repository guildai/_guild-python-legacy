#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-output",
    srcs = ["guild-output.html"],
    path = "/guild-output",
    deps = [
        "//components/guild-component-panel",
        "//components/guild-datatable',/guild-datatable.html">
        "//components/guild-filter-input',/guild-filter-input.html">
        "//components/guild-imports:d3",
        "//components/guild-run:guild-run-data-listener",
        "@org_polymer_paper_toolbar",
    ],
)
