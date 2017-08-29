#-*-python-*-

load("@io_bazel_rules_closure//closure:defs.bzl", "web_library_external")

def guild_polymer_workspace():

    web_library_external(
        name = "org_polymer_app_route",
        licenses = ["notice"],  # BSD-3-Clause
        sha256 = "8f66386d29b09f1de1058a4233d2a63d99c3c466e89533a295dba644818f7998",
        urls = [
            "http://mirror.bazel.build/github.com/PolymerElements/app-route/archive/v1.0.1.tar.gz",
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
            "http://mirror.bazel.build/github.com/PolymerElements/iron-location/archive/v1.0.0.tar.gz",
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
