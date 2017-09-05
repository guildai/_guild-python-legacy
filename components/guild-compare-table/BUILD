package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-compare-table",
    srcs = ["guild-compare-table.html"],
    path = "/guild-compare-table",
    deps = [
        ":compare-table-support",
        "//components/guild-filter-input",
        "//components/guild-run:guild-run-compare-data-listener",
        "//components/guild-styles",
        "@org_polymer_paper_material",
        "@org_polymer_paper_toggle_button",
        "@org_polymer_paper_toolbar",
    ],
)

ts_web_library(
    name = "compare-table-support",
    srcs = [
        "compare-table-support.html",
        "compare-table.ts",
    ],
    path = "/guild-compare-table",
    deps = [
        ":guild-compare-table-select",
        "//components/guild-run",
        "//components/guild-util",
        "//components/guild-imports:datatables",
        "//components/guild-imports:jquery",
        "@org_guildai_fa_awesome",
    ],
)

ts_web_library(
    name = "guild-compare-table-select",
    srcs = [
        "guild-compare-table-select.html",
    ],
    path = "/guild-compare-table",
    deps = [
        "//components/guild-checkbox",
    ],
)
