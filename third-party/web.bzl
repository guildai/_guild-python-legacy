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

    filegroup_external(
        name = "com_jquery",
        licenses = ["notice"],  # MIT
        sha256_urls = {
            "87083882cc6015984eb0411a99d3981817f5dc5c90ba24f0940420c5548d82de": [
                "https://code.jquery.com/jquery-3.2.1.min.js",
            ],
        },
        rename = {"jquery-3.2.1.min.js": "jquery.min.js"},
    )

    web_library_external(
        name = "net_datatables",
        licenses = ["notice"],  # MIT
        sha256 = "ee0ad0063cac4c04c20644e7bb9e8950a67346eafdcc2051a414fc95a0f4ab36",
        urls = [
            "https://github.com/DataTables/Dist-DataTables/archive/1.10.15.zip",
        ],
        strip_prefix = "Dist-DataTables-1.10.15",
        path = "/datatables.net",
        srcs = [
            "js/jquery.dataTables.min.js",
        ],
    )

    web_library_external(
        name = "net_datatables_dt",
        licenses = ["notice"],  # MIT
        sha256 = "91ea05c88003c12e967f8d5318af0c4deabf836f70a7a3c9d165ec01333e288c",
        urls = [
            "https://github.com/DataTables/Dist-DataTables-DataTables/archive/1.10.15.zip",
        ],
        strip_prefix = "Dist-DataTables-DataTables-1.10.15",
        path = "/datatables.net-dt",
        srcs = [
            "css/jquery.dataTables.min.css",
            "images/sort_both.png",
            "images/sort_asc.png",
            "images/sort_desc.png",
            "images/sort_asc_disabled.png",
            "images/sort_desc_disabled.png",
        ],
    )

    web_library_external(
        name = "org_jsondiffpatch",
        licenses = ["notice"],  # MIT
        sha256 = "0a7d984a500626adc6abb68901b97a053443325bd04cda75840529a90bbc5610",
        urls = [
            "https://github.com/benjamine/jsondiffpatch/archive/v0.2.4.zip",
        ],
        strip_prefix = "jsondiffpatch-0.2.4",
        path = "/jsondiffpatch",
        srcs = [
            "public/build/jsondiffpatch.min.js",
            "public/build/jsondiffpatch-formatters.min.js",
        ],
    )
    
