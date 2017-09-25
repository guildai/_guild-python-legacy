package(default_visibility = ["//visibility:public"])

sh_binary(
    name = "guild",
    srcs = ["//scripts:guild-exe"],
    data = [
        ":guild_main",
    ]
)

py_library(
    name = "guild_main",
    srcs = ["guild_main.py"],
    deps = [
        ":check_cmd",
        ":evaluate_cmd",
        ":info_cmd",
        ":install_cmd",
        ":prepare_cmd",
        ":project_cmd",
        ":query_cmd",
        ":runs_cmd",
        ":search_cmd",
        ":sources_cmd",
        ":sync_cmd",
        ":train_cmd",
        ":view_cmd",
        "@org_click",
    ]
)

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_library(
    name = "app",
    srcs = ["app.py"],
    deps = [
        ":__init__",
        "//guild/plugins"
    ]
)

py_library(
    name = "check_cmd",
    srcs = ["check_cmd.py"],
    data = [
        "//scripts:nvidia-tools-check",
        "//scripts:tensorflow-check",
    ],
    deps = [
        ":app",
        ":cli",
        ":test",
    ],
)

py_library(
    name = "cli",
    srcs = ["cli.py"],
    deps = [
        ":app",
    ],
)

py_library(
    name = "cmd_support",
    srcs = ["cmd_support.py"],
    deps = [
        ":app",
        ":cli",
        ":run",
        ":util",
    ],
)

py_library(
    name = "db",
    srcs = ["db.py"],
    deps = [
        ":opdir",
        ":util",
    ],
)

py_library(
    name = "evaluate_cmd",
    srcs = ["evaluate_cmd.py"],
    deps = [
    ],
)

py_library(
    name = "log",
    srcs = ["log.py"],
)

py_library(
    name = "op",
    srcs = ["op.py"],
    deps = [
        ":app",
        ":db",
        ":op_support",
        ":opdir",
        ":util",
    ],
)

py_library(
    name = "op_support",
    srcs = ["op_support.py"],
    deps = [
        ":system",
        ":util",
    ],
)

py_library(
    name = "op_util",
    srcs = ["op_util.py"],
    deps = [
        ":opdir",
        ":util",
    ],
)

py_library(
    name = "opdir",
    srcs = ["opdir.py"],
    deps = [
        ":util",
    ],
)

py_library(
    name = "prepare_cmd",
    srcs = ["prepare_cmd.py"],
    deps = [
        ":cli",
        ":cmd_support",
        ":op",
        ":op_support",
    ],
)

py_library(
    name = "project",
    srcs = ["project.py"],
    deps = [
        "@org_pyyaml",
    ]
)

py_library(
    name = "project_cmd",
    srcs = ["project_cmd.py"],
    deps = [
        ":cmd_support",
        ":view",
        "@org_pyyaml",
    ],
)

py_library(
    name = "project_util",
    srcs = ["project_util.py"],
    deps = [
        ":project",
        ":util",
    ],
)

py_library(
    name = "run",
    srcs = ["run.py"],
    deps = [
        ":opdir",
        ":project_util",
    ],
)

py_library(
    name = "query_cmd",
    srcs = ["query_cmd.py"],
    deps = [
        ":cmd_support",
        ":db",
        ":op_util",
    ],
)

py_library(
    name = "runs_cmd",
    srcs = ["runs_cmd.py"],
    deps = [
        ":cmd_support",
        ":op_util",
        ":project_util",
        ":run",
    ],
)

py_library(
    name = "system",
    srcs = ["system.py"],
    data = [
        "//scripts:gpu-attrs",
        "//scripts:sys-attrs",
    ],
    deps = [
        ":app",
        ":log",
    ],
)

py_library(
    name = "task_support",
    srcs = ["task_support.py"],
)

py_library(
    name = "tensorboard_proxy",
    srcs = ["tensorboard_proxy.py"],
    data = [
        "@org_tensorflow_tensorboard//tensorboard",
    ],
    deps = [
        ":log",
    ],
)

py_library(
    name = "tensorflow_support",
    srcs = ["tensorflow_support.py"],
    data = [
        "//scripts:tensorflow-attrs",
    ],
    deps = [
        ":app",
        ":log",
    ],
)

py_library(
    name = "test",
    srcs = ["test.py"],
    data = [
        "//tests",
    ],
    deps = [
        ":app",
    ],
)

py_library(
    name = "train_cmd",
    srcs = ["train_cmd.py"],
    deps = [
        ":cmd_support",
        ":op",
        ":project_util",
        "//guild/tasks:log_flags",
        "//guild/tasks:log_system_attrs",
        "//guild/tasks:snapshot_project",
        "//guild/tasks:tensorflow_events",
        "//guild/tasks:op_stats",
        "//guild/tasks:sys_stats",
        "//guild/tasks:gpu_stats",
    ]
)

py_library(
    name = "util",
    srcs = ["util.py"],
)

py_library(
    name = "view",
    srcs = ["view.py"],
    data = [
        "//include:project-base.yml",
    ],
    deps = [
        ":db",
        ":log",
        ":op_util",
        ":project_util",
        ":run",
    ],
)

py_library(
    name = "view_cmd",
    srcs = ["view_cmd.py"],
    data = [
        "//include:project-base.yml",
        "//assets",
        "//components:guild-bin.html",
    ],
    deps = [
        ":cli",
        ":cmd_support",
        ":tensorboard_proxy",
        ":view",
        ":view_http",
    ],
)

py_library(
    name = "view_http",
    srcs = ["view_http.py"],
    deps = [
        ":app",
        ":project_util",
        ":view",
        "@org_pocoo_werkzeug",
    ],
)

py_library(
    name = "sources_cmd",
    srcs = ["sources_cmd.py"],
    deps = [
        ":cmd_support",
        ":cli",
        ":user",
    ],
)

py_library(
    name = "source",
    srcs = ["source.py"],
    deps = [
        ":log",
        ":user",
        ":util",
        "@org_pyyaml",
        "@org_semantic_version",
    ],
)

py_library(
    name = "user",
    srcs = ["user.py"],
    deps = [
        "@org_pyyaml",
    ],
)

py_library(
    name = "sync_cmd",
    srcs = ["sync_cmd.py"],
    deps = [
        ":cmd_support",
        ":cli",
        ":git",
        ":user",
    ]
)

py_library(
    name = "git",
    srcs = ["git.py"],
    deps = [
        ":log",
    ],
)

py_library(
    name = "search_cmd",
    srcs = ["search_cmd.py"],
    deps = [
        ":cmd_support",
        ":cli",
        ":source",
    ]
)

py_library(
    name = "info_cmd",
    srcs = ["info_cmd.py"],
    deps = [
        ":cmd_support",
        ":source_cmd_support",
    ]
)

py_library(
    name = "install_cmd",
    srcs = ["install_cmd.py"],
    deps = [
        ":cmd_support",
        ":source_cmd_support",
        ":wget",
    ]
)

py_library(
    name = "source_cmd_support",
    srcs = ["source_cmd_support.py"],
    deps = [
        ":source",
    ]
)

py_library(
    name = "wget",
    srcs = ["wget.py"],
    deps = [
        ":util",
        "@org_tqdm",
    ]
)
