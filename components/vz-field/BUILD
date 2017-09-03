package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "vz-field",
    srcs = ["vz-field.html"],
    path = "/vz-field",
    deps = [
        "//components/guild-icons",
        "@org_polymer_paper_card",
        "@org_polymer_paper_styles",
    ],
)

web_library(
    name = "demo",
    srcs = ["demo.html"],
    path = "/vz-field",
    deps = [
        ":vz-field",
        "@org_polymer_webcomponentsjs",
        "@org_polymer_iron_demo_helpers",
    ]
)
