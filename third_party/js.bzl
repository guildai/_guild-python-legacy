#-*-python-*-

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
