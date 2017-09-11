package(default_visibility = ["//visibility:public"])

load("//components:vulcanize.bzl", "guild_html_binary")
load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

guild_html_binary(
    name = "guild-bin",
    input_path = "/guild.html",
    output_path = "/guild-bin.html",
    deps = [":guild"],
)

ts_web_library(
    name = "guild",
    srcs = [
        "guild.html",
    ],
    path = "/",
    deps = [
        "//assets",
        "//components/guild-view",
        "@org_polymer_webcomponentsjs",
    ],
)
