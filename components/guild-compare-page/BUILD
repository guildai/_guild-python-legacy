package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-compare-page",
    srcs = ["guild-compare-page.html"],
    path = "/guild-compare-page",
    deps = [
        "//components/guild-compare-components",
        "//components/guild-compare-table",
        "//components/guild-page-header",
        "//components/guild-project",
    ],
)
