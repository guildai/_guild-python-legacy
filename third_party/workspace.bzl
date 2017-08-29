#-*-python-*-

load("@org_tensorflow_tensorboard//third_party:workspace.bzl", "tensorboard_workspace")
load("//third_party:python.bzl", "guild_python_workspace")
load("//third_party:polymer.bzl", "guild_polymer_workspace")
load("//third_party:js.bzl", "guild_js_workspace")

def third_party_workspace():

    tensorboard_workspace()
    guild_python_workspace()
    guild_polymer_workspace()
    guild_js_workspace()
