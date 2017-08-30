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
        ":guild-view-styles",
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
        ":guild-view-app-toolbar",
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
        "@org_polymer_iron_icon",
        "@org_polymer_paper_item",
        "@org_polymer_paper_menu",
        "@org_polymer_paper_toolbar",
    ],
)

web_library(
    name = "guild-view-app-toolbar",
    srcs = ["guild-view-app-toolbar.html"],
    path = "/guild-view",
    deps = [
        ":guild-view-app-menu",
        "//components/guild-icons",
        "@org_polymer_app_layout",
        "@org_polymer_iron_icon",
        "@org_polymer_paper_tabs",
    ],
)

web_library(
    name = "guild-view-styles",
    srcs = ["guild-view-styles.html"],
    path = "/guild-view",
    deps = [
    ],
)
