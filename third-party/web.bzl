#-*-python-*-

load("@io_bazel_rules_closure//closure:defs.bzl", "filegroup_external")
load("@io_bazel_rules_closure//closure:defs.bzl", "web_library_external")

def guild_web_workspace():

    web_library_external(
        name = "com_numeraljs",
        licenses = ["notice"],  # MIT
        sha256 = "f5366e37c32e09501392276ba9f8c14e0f3fc40bb7b42102363f5e7d58082e8a",
        urls = [
            "https://github.com/adamwdraper/Numeral-js/archive/2.0.6.tar.gz",
        ],
        strip_prefix = "Numeral-js-2.0.6",
        path = "/numeral",
        srcs = [
            "numeral.js",
        ],
    )

    filegroup_external(
        name = "org_d3js_time_format",
        licenses = ["notice"],  # BSD-3-Clause
        sha256_urls_extract = {
            "49169bd070eb06744628ad52b8e46d1fd54e17b6e90d974e0ba47353cd8d65f4": [
                "https://github.com/d3/d3-time-format/releases/download/v2.0.5/d3-time-format.zip",
            ],
        },
    )

    filegroup_external(
        name = "org_twbs_bootstrap",
        licenses = ["notice"],  # MIT
        sha256_urls_extract = {
            "89ad718413a3f7ff9a0e05b2909365532385a81ae2844f4ba3ddef519f39f14b": [
                "https://github.com/twbs/bootstrap/releases/download/v4.0.0-beta/bootstrap-4.0.0-beta-dist.zip",
            ],
        },
    )

    web_library_external(
        name = "org_fontawesome",
        licenses = ["notice"],  # ???
        sha256 = "de512ba0e1dead382bbfce372cde74b3f18971d876fffb635ee9333f0db05d43",
        urls = [
            "https://github.com/FortAwesome/Font-Awesome/archive/v4.7.0.tar.gz",
        ],
        strip_prefix = "Font-Awesome-4.7.0",
        path = "/font-awesome",
        srcs = [
            "css/font-awesome.css",
            "css/font-awesome.css.map",
            "css/font-awesome.min.css",
            "fonts/FontAwesome.otf",
            "fonts/fontawesome-webfont.eot",
            "fonts/fontawesome-webfont.svg",
            "fonts/fontawesome-webfont.ttf",
            "fonts/fontawesome-webfont.woff",
            "fonts/fontawesome-webfont.woff2",
        ],
        suppress = ["strictDependencies"],
    )
