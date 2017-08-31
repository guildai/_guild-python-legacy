#-*-python-*-

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
