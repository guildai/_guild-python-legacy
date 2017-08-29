#-*-python-*-

package(default_visibility = ["//visibility:public"])

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library")

web_library(
    name = "guild-view",
    srcs = ["guild-view.html"],
    path = "/guild-view",
    deps = [
        ":guild-view-route",
        ":guild-view-app-layout",
        ":guild-view-page",
        "//components/guild-env",
        "@org_polymer_app_route",
    ],
)

web_library(
    name = "guild-view-route",
    srcs = ["guild-view-route.html"],
    path = "/guild-view",
    deps = [
    ],
)

web_library(
    name = "guild-view-app-layout",
    srcs = ["guild-view-app-layout.html"],
    path = "/guild-view",
    deps = [
        ":guild-view-app-menu",
        "@org_polymer_app_layout",
        "@org_polymer_iron_pages",
        "@org_polymer_paper_icon_button",
    ],
)

web_library(
    name = "guild-view-page",
    srcs = ["guild-view-page.html"],
    path = "/guild-view",
    deps = [
    ],
)

web_library(
    name = "guild-view-app-menu",
    srcs = ["guild-view-app-menu.html"],
    path = "/guild-view",
    deps = [
        "//components/guild-icons",
    ],
)
