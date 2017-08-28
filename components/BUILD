#-*-python-*-

package(default_visibility = ["//guild:visibility"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")
load("@org_tensorflow_tensorboard//tensorboard/defs:vulcanize.bzl", "tensorboard_html_binary")

tensorboard_html_binary(
    name = "index",
    input_path = "/guild.html",
    output_path = "/index.html",
    deps = [":guild"],
)

ts_web_library(
    name = "guild",
    srcs = [
        "guild.html",
    ],
    path = "/",
)
