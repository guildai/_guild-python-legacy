#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-datatable",
    srcs = [
        "guild-datatable.html",
        "guild-datatable.js",
    ],
    path = "/guild-datatable",
    deps = [
        ":datatable-col",
        ":datatable-styles",
        "//components/guild-imports:datatables",
        "//components/guild-imports:jquery",
    ],
)

web_library(
    name = "datatable-col",
    srcs = ["datatable-col.html"],
    path = "/guild-datatable",
    deps = [
        "@org_polymer",
    ],
)

web_library(
    name = "datatable-styles",
    srcs = ["datatable-styles.html"],
    path = "/guild-datatable",
    deps = [
    ],
)
