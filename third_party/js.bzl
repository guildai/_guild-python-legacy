#-*-python-*-

load("@io_bazel_rules_closure//closure:defs.bzl", "filegroup_external")
load("@io_bazel_rules_closure//closure:defs.bzl", "web_library_external")

def guild_js_workspace():

    web_library_external(
        name = "com_numeraljs",
        licenses = ["notice"],  # MIT
        sha256 = "f5366e37c32e09501392276ba9f8c14e0f3fc40bb7b42102363f5e7d58082e8a",
        urls = [
            "http://mirror.bazel.build/github.com/adamwdraper/Numeral-js/archive/2.0.6.tar.gz",
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
                "http://mirror.bazel.build/https://github.com/d3/d3-time-format/releases/download/v2.0.5/d3-time-format.zip",
                "https://github.com/d3/d3-time-format/releases/download/v2.0.5/d3-time-format.zip",
            ],
        },
    )
