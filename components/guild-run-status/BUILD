package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-run-status",
    srcs = ["guild-run-status.html"],
    path = "/guild-run-status",
    deps = [
        "//components/guild-run",
        "//components/guild-styles",
        "@org_polymer",
        "@org_guildai_fa_awesome",
    ],
)

ts_web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/guild-run-status",
    deps = [
        ":guild-run-status",
        "//components/guild-env",
        "//components/guild-view/demo:demo-data",
        "@org_polymer_webcomponentsjs",
        "@org_polymer_app_route",
    ]
)
