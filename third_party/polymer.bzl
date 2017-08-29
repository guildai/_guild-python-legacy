#-*-python-*-

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library_external")

def guild_polymer_workspace():

    web_library_external(
        name = "org_polymer_app_route",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "8f66386d29b09f1de1058a4233d2a63d99c3c466e89533a295dba644818f7998",
        urls = [
            "https://github.com/PolymerElements/app-route/archive/v1.0.1.tar.gz",
        ],
        strip_prefix = "app-route-1.0.1",
        path = "/app-route",
        srcs = [
            "app-location.html",
            "app-route-converter-behavior.html",
            "app-route-converter.html",
            "app-route.html",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_location",
        ],
    )

    web_library_external(
        name = "org_polymer_iron_location",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "df92e29817409a9f058d67b5a99b0fb406e03045c762531d0afa493e719660d8",
        urls = [
            "https://github.com/PolymerElements/iron-location/archive/v1.0.0.tar.gz",
        ],
        strip_prefix = "iron-location-1.0.0",
        path = "/iron-location",
        srcs = [
            "iron-location.html",
            "iron-query-params.html",
        ],
        deps = ["@org_polymer"],
    )

    web_library_external(
        name = "org_polymer_app_layout",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "5c4f722da352b216f3df894bf97f496c28ca1958f6f39f588636df6a964add22",
        urls = [
            "https://github.com/PolymerElements/app-layout/archive/v1.0.1.tar.gz",
        ],
        strip_prefix = "app-layout-1.0.1",
        path = "/app-layout",
        srcs = [
            "app-header/app-header.html",
            "app-header-layout/app-header-layout.html",
            "app-drawer/app-drawer.html",
            "app-drawer-layout/app-drawer-layout.html",
            "app-scroll-effects/app-scroll-effects.html",
            "app-scroll-effects/app-scroll-effects-behavior.html",
            "app-scroll-effects/effects/resize-snapped-title.html",
            "app-scroll-effects/effects/blend-background.html",
            "app-scroll-effects/effects/parallax-background.html",
            "app-scroll-effects/effects/material.html",
            "app-scroll-effects/effects/waterfall.html",
            "app-scroll-effects/effects/resize-title.html",
            "app-scroll-effects/effects/fade-background.html",
            "app-box/app-box.html",
            "app-scrollpos-control/app-scrollpos-control.html",
            "app-grid/app-grid-style.html",
            "app-toolbar/app-toolbar.html",
            "helpers/helpers.html",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_flex_layout",
            "@org_polymer_iron_resizable_behavior",
            "@org_polymer_iron_scroll_target_behavior",
            "@org_polymer_iron_media_query",
        ],
    )

    web_library_external(
        name = "org_polymer_iron_media_query",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "93c145610bd4401c3969e87a62f18bc5def8f850ac46a236c7b6b270ed59cef3",
        urls = [
            "https://github.com/PolymerElements/iron-media-query/archive/v1.0.8.tar.gz",
        ],
        strip_prefix = "iron-media-query-1.0.8",
        path = "/iron-media-query",
        srcs = [
            "iron-media-query.html",
        ],
        deps = ["@org_polymer"],
    )

    web_library_external(
        name = "org_polymer_iron_pages",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "9a1b8e6b2d1dd11f94d7aa674c811a1e6b7dd766678e3650228deb109520612a",
        urls = [
            "https://github.com/PolymerElements/iron-pages/archive/v1.0.9.tar.gz",
        ],
        strip_prefix = "iron-pages-1.0.9",
        path = "/iron-pages",
        srcs = [
            "iron-pages.html",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_resizable_behavior",
            "@org_polymer_iron_selector",
        ],
    )
