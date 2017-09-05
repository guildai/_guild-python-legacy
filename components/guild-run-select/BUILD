package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-run-select",
    srcs = ["guild-run-select.html"],
    path = "/guild-run-select",
    deps = [
        ":guild-run-select-item",
        ":guild-run-select-error",
        "@org_polymer_paper_dropdown_menu",
        "@org_polymer_paper_listbox",
    ],
)

ts_web_library(
    name = "guild-run-select-item",
    srcs = ["guild-run-select-item.html"],
    path = "/guild-run-select",
    deps = [
        "@org_guildai_fa_awesome",
        "//components/guild-styles",
        "//components/guild-run",
        "@org_polymer_paper_item",
    ],
)

ts_web_library(
    name = "guild-run-select-error",
    srcs = ["guild-run-select-error.html"],
    path = "/guild-run-select",
    deps = [
        "@org_guildai_fa_awesome",
        "@org_polymer_paper_button",
        "@org_polymer_paper_tooltip",
    ],
)
