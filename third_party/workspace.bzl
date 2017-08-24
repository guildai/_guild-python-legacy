#-*-python-*-

def third_party_workspace():
    native.new_http_archive(
        name = "org_pocoo_werkzeug",
        urls = [
            "http://mirror.bazel.build/pypi.python.org/packages/b7/7f/44d3cfe5a12ba002b253f6985a4477edfa66da53787a2a838a40f6415263/Werkzeug-0.11.10.tar.gz",
            "https://pypi.python.org/packages/b7/7f/44d3cfe5a12ba002b253f6985a4477edfa66da53787a2a838a40f6415263/Werkzeug-0.11.10.tar.gz",
        ],
        strip_prefix = "Werkzeug-0.11.10",
        sha256 = "cc64dafbacc716cdd42503cf6c44cb5a35576443d82f29f6829e5c49264aeeee",
        build_file = "//third_party:werkzeug.BUILD",
    )
