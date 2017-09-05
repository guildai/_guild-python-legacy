package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")
load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

tensorboard_html_binary(
    name = "index",
    input_path = "/guild.html",
    output_path = "/index.html",
    deps = [":guild"],
)

guild_deps = [
    "//assets",
    "//components/guild-view",
    "@org_polymer_webcomponentsjs",
]

ts_web_library(
    name = "guild",
    srcs = [
        "guild.html",
    ],
    path = "/",
    deps = guild_deps,
)

ts_web_library(
    name = "guild-demo",
    srcs = [
        "guild.html",
    ],
    path = "/",
    deps = guild_deps + [
        "//components/guild-view/demo:demo-data"
    ],
)
