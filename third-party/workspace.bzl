#-*-python-*-

load("@org_tensorflow_tensorboard//third_party:workspace.bzl", "tensorboard_workspace")
load("//third-party:python.bzl", "guild_python_workspace")
load("//third-party:polymer.bzl", "guild_polymer_workspace")
load("//third-party:web.bzl", "guild_web_workspace")
load("//third-party:typings.bzl", "guild_typings_workspace")

def third_party_workspace():
    tensorboard_workspace()
    guild_python_workspace()
    guild_polymer_workspace()
    guild_web_workspace()
    guild_typings_workspace()
