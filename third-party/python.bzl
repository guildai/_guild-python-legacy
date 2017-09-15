#-*-python-*-

def guild_python_workspace():

    native.new_http_archive(
        name = "org_pyyaml",
        build_file = "//third-party:pyyaml.BUILD",
        urls = [
            "https://pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz",
        ],
        strip_prefix = "PyYAML-3.12",
        sha256 = "592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab",
    )

    native.new_http_archive(
        name = "org_psutil",
        build_file = "//third-party:psutil.BUILD",
        urls = [
            "https://pypi.python.org/packages/57/93/47a2e3befaf194ccc3d05ffbcba2cdcdd22a231100ef7e4cf63f085c900b/psutil-5.2.2.tar.gz"
        ],
        strip_prefix = "psutil-5.2.2",
        sha256 = "44746540c0fab5b95401520d29eb9ffe84b3b4a235bd1d1971cbe36e1f38dd13",
    )

    native.new_http_archive(
        name = "org_semantic_version",
        build_file = "//third-party:semantic_version.BUILD",
        urls = [
            "https://pypi.python.org/packages/72/83/f76958017f3094b072d8e3a72d25c3ed65f754cc607fdb6a7b33d84ab1d5/semantic_version-2.6.0.tar.gz"
        ],
        strip_prefix = "semantic_version-2.6.0",
        sha256 = "2a4328680073e9b243667b201119772aefc5fc63ae32398d6afafff07c4f54c0",
    )

    native.new_http_archive(
        name = "org_tqdm",
        build_file = "//third-party:tqdm.BUILD",
        urls = [
            "https://pypi.python.org/packages/01/f7/2058bd94a903f445e8ff19c0af64b9456187acab41090ff2da21c7c7e193/tqdm-4.15.0.tar.gz"
        ],
        strip_prefix = "tqdm-4.15.0",
        sha256 = "6ec1dc74efacf2cda936b4a6cf4082ce224c76763bdec9f17e437c8cfcaa9953",
    )
