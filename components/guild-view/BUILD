#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-view",
    srcs = [
        "guild-view.html",
        "guild-view-route.html",
    ],
    path = "/guild-view",
    deps = [
        "//components/guild-env",
        "@org_polymer_app_route",
    ],
)

web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/guild-view",
    deps = [
        ":guild-view",
        "@org_polymer_webcomponentsjs",
        "@org_polymer_iron_demo_helpers",
    ],
)
