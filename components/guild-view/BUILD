package(default_visibility = ["//visibility:public"])

load("@org_tensorflow_tensorboard//tensorboard/defs:web.bzl", "ts_web_library")

ts_web_library(
    name = "guild-view",
    srcs = ["guild-view.html"],
    path = "/guild-view",
    deps = [
        ":guild-view-route",
        ":guild-view-app-layout",
        ":guild-view-page",
        ":guild-view-styles",
        ":guild-view-fullscreen",
        "//components/guild-env",
        "//components/guild-components-page",
        "//components/guild-compare-page",
        "@org_polymer_app_route",
    ],
)

ts_web_library(
    name = "guild-view-route",
    srcs = ["guild-view-route.html"],
    path = "/guild-view",
    deps = [
    ],
)

ts_web_library(
    name = "guild-view-app-layout",
    srcs = [
        "guild-view-app-layout.html",
        "app-layout-util.ts",
    ],
    path = "/guild-view",
    deps = [
        ":guild-view-app-menu",
        ":guild-view-app-toolbar",
        "@org_polymer_app_layout",
        "@org_polymer_iron_pages",
        "@org_polymer_paper_icon_button",
    ],
)

ts_web_library(
    name = "guild-view-page",
    srcs = ["guild-view-page.html"],
    path = "/guild-view",
    deps = [
    ],
)

ts_web_library(
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

ts_web_library(
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

ts_web_library(
    name = "guild-view-styles",
    srcs = ["guild-view-styles.html"],
    path = "/guild-view",
    deps = [
    ],
)

ts_web_library(
    name = "guild-view-page-overlay",
    srcs = ["guild-view-page-overlay.html"],
    path = "/guild-view",
    deps = [
        "@org_polymer_iron_resizable_behavior",
    ],
)

ts_web_library(
    name = "fullscreen-behavior",
    srcs = [
        "fullscreen-behavior.html",
        "fullscreen.ts"
    ],
    path = "/guild-view",
    deps = [
    ],
)

ts_web_library(
    name = "guild-view-fullscreen",
    srcs = ["guild-view-fullscreen.html"],
    path = "/guild-view",
    deps = [
        "@org_polymer_iron_overlay_behavior",
    ],
)
