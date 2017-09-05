package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-run-dropdown-menu",
    srcs = ["guild-run-dropdown-menu.html"],
    path = "/guild-run-dropdown-menu",
    deps = [
        "//components/guild-run",
        "@org_polymer_paper_dropdown_menu",
        "@org_polymer_paper_listbox",
        "@org_polymer_paper_item",
    ],
)
