#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "demo",
    srcs = ["index.html"],
    path = "/guild-view/demo",
    deps = [
        "//components/guild-view",
        "@org_polymer_webcomponentsjs",
        "@org_polymer_iron_demo_helpers",
        ":demo_data",
    ],
)

web_library(
    name = "demo_data",
    srcs = glob(["data/**"]),
    path = "/",
)
