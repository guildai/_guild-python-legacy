package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-datatable",
    srcs = [
        "guild-datatable.html",
        "guild-datatable.ts",
    ],
    path = "/guild-datatable",
    deps = [
        ":datatable-col",
        ":datatable-styles",
        "//components/guild-imports:datatables",
        "//components/guild-imports:jquery",
    ],
)

ts_web_library(
    name = "datatable-col",
    srcs = ["datatable-col.html"],
    path = "/guild-datatable",
    deps = [
        "@org_polymer",
    ],
)

ts_web_library(
    name = "datatable-styles",
    srcs = ["datatable-styles.html"],
    path = "/guild-datatable",
    deps = [
    ],
)
