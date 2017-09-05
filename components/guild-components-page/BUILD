package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-components-page",
    srcs = ["guild-components-page.html"],
    path = "/guild-components-page",
    deps = [
        "//components/guild-imports:bootstrap-grid",
        "//components/guild-project",
        "//components/guild-run",
        "//components/guild-run-select-page-header",
        "//components/guild-styles",
        "//components/guild-view:guild-view-page-overlay",
        "//components/guild-attrs",
        "//components/guild-fields",
        "//components/guild-flags",
        "//components/guild-output",
        "//components/guild-series",
        "@org_polymer_paper_card",
    ],
)
