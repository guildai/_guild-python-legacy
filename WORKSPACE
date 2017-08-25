#-*-python-*-

workspace(name = "ai_guild_guild")

http_archive(
    name = "io_bazel_rules_closure",
    sha256 = "e9e2538b1f7f27de73fa2914b7d2cb1ce2ac01d1abe8390cfe51fb2558ef8b27",
    strip_prefix = "rules_closure-4c559574447f90751f05155faba4f3344668f666",
    urls = [
        "http://mirror.bazel.build/github.com/bazelbuild/rules_closure/archive/4c559574447f90751f05155faba4f3344668f666.tar.gz",
        "https://github.com/bazelbuild/rules_closure/archive/4c559574447f90751f05155faba4f3344668f666.tar.gz",  # 2017-06-21
    ],
)

load("@io_bazel_rules_closure//closure:defs.bzl", "closure_repositories")

closure_repositories()

http_archive(
    name = "org_tensorflow_tensorboard",
    sha256 = "9379e711f71c5ba537f047edb60bb2eaca268f75425cd0dd16e3aba48907f2a0",
    strip_prefix = "tensorboard-2da8a6d6b79b29b192dac8d227ab82ad3479b1fc",
    urls = [
        "http://mirror.bazel.build/github.com/tensorflow/tensorboard/archive/2da8a6d6b79b29b192dac8d227ab82ad3479b1fc.tar.gz",
        "https://github.com/tensorflow/tensorboard/archive/2da8a6d6b79b29b192dac8d227ab82ad3479b1fc.tar.gz",
    ],
)

load("//third_party:workspace.bzl", "third_party_workspace")

third_party_workspace()
