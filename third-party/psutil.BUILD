#-*-python-*-

py_library(
    name = "org_psutil",
    srcs = glob(["psutil/*.py", "psutil/*.so"]),
    visibility = ["//visibility:public"],
    data = [":psutil_native"],
)

genrule(
    name = "psutil_native",
    srcs = glob([
        "setup.py",
        "README.rst",
        "psutil/*.py",
        "psutil/*.c",
    ]),
    outs = ["psutil/_psutil_linux.so",
            "psutil/_psutil_posix.so",
    ],
    cmd = ("pushd `dirname $(location setup.py)` && " +
           "python setup.py build_ext -i && " +
           "popd && " +
           "cp `dirname $(location setup.py)`/psutil/_psutil_linux.so $(@D)/psutil/ && " +
           "cp `dirname $(location setup.py)`/psutil/_psutil_posix.so $(@D)/psutil/")
)
