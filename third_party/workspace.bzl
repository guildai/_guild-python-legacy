#-*-python-*-

load("@org_tensorflow_tensorboard//third_party:workspace.bzl", "tensorboard_workspace")

def third_party_workspace():

    tensorboard_workspace()

    native.new_http_archive(
        name = "org_pyyaml",
        urls = [
            "http://mirror.bazel.build/pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz",
            "https://pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz",
        ],
        strip_prefix = "PyYAML-3.12",
        sha256 = "592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab",
        build_file = "//third_party:pyyaml.BUILD",
    )

    native.new_http_archive(
        name = "org_psutil",
        urls = [
            "http://mirror.bazel.build/pypi.python.org/packages/57/93/47a2e3befaf194ccc3d05ffbcba2cdcdd22a231100ef7e4cf63f085c900b/psutil-5.2.2.tar.gz",
            "https://pypi.python.org/packages/57/93/47a2e3befaf194ccc3d05ffbcba2cdcdd22a231100ef7e4cf63f085c900b/psutil-5.2.2.tar.gz"
        ],
        strip_prefix = "psutil-5.2.2",
        sha256 = "44746540c0fab5b95401520d29eb9ffe84b3b4a235bd1d1971cbe36e1f38dd13",
        build_file = "//third_party:psutil.BUILD",
    )

    native.bind(
        name = "tensorboard",
        actual = "@org_tensorflow_tensorboard//tensorboard:tensorboard",
    )

    native.bind(
        name = "werkzeug",
        actual = "@org_pocoo_werkzeug",
    )

    native.bind(
        name = "yaml",
        actual = "@org_pyyaml",
    )

    native.bind(
        name = "psutil",
        actual = "@org_psutil",
    )
