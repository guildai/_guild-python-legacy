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

    web_library_external(
        name = "org_pkaske_font_awesome_polymer_icons",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "7c83916b54b5d16460def96181d864c698a803567cc34abdbf62faca9da7ed81",
        urls = [
            "https://github.com/pkaske/font-awesome-polymer-icons/archive/v4.4.0.tar.gz",
        ],
        strip_prefix = "font-awesome-polymer-icons-4.4.0",
        path = "/font-awesome-polymer-icons",
        srcs = [
            "fa-all.html",
            "fa-brand.html",
            "fa-chart.html",
            "fa-currency.html",
            "fa-directional.html",
            "fa-file-type.html",
            "fa-form-control.html",
            "fa-gender.html",
            "fa-hand.html",
            "fa-medical.html",
            "fa-payment.html",
            "fa-spinner.html",
            "fa-text-editor.html",
            "fa-transportation.html",
            "fa-video-player.html",
            "fa-web-application.html",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_icon",
            "@org_polymer_iron_iconset_svg",
        ],
    )

    web_library_external(
        name = "org_guildai_fa_awesome",
        licenses = ["notice"],  # MIT
        sha256 = "b156e7c9c778156332585ad36273fd7bfa1a99fe490849a5afa66226128796e7",
        urls = [
            "https://github.com/guildai/fa-awesome/archive/1.3.2.tar.gz",
        ],
        strip_prefix = "fa-awesome-1.3.2",
        path = "/fa-awesome",
        srcs = [
            "fa-awesome.html",
            "fa-awesome.css",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_flex_layout",
            "@org_polymer_neon_animation",
            "@org_fontawesome",
        ],
    )

    web_library_external(
        name = "org_polymer_paper_card",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "bcfecab0d28dcc5f7b8dd784d71b3c5a90c645fc984f7f57974211b82eccc31b",
        urls = [
            "https://github.com/PolymerElements/paper-card/archive/v1.1.6.tar.gz",
        ],
        strip_prefix = "paper-card-1.1.6",
        path = "/paper-card",
        srcs = [
            "paper-card.html",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_flex_layout",
            "@org_polymer_iron_image",
            "@org_polymer_paper_material",
            "@org_polymer_paper_styles",
        ],
    )

    web_library_external(
        name = "org_polymer_iron_image",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "c6e8b4840e95314bc452e270d01dd69eedd7362c4babd78f3d63be7b35aeaa6a",
        urls = [
            "https://github.com/PolymerElements/iron-image/archive/v1.2.6.zip",
        ],
        strip_prefix = "iron-image-1.2.6",
        path = "/iron-image",
        srcs = [
            "iron-image.html",
        ],
        deps = [
            "@org_polymer",
            "@org_polymer_iron_flex_layout",
        ],
    )
