# This package takes Vulcanize in house for a couple reasons:
#
# - We need to replace JSoup's aggressive DOM mangling with something
#   that doesn't break Polymer templates inside various HTML elements
#   (e.g. tables)
#
# - We need to control our own 'externs.js', which is how Vulcanize is
#   inserting various top-level declarations or other structures needed by
#   non ES6 module JavaScript code
#
# This is a *lot* to bring in house and duplicate and so is a vector for
# ongoing bugs.
#
# Packages/labels to manually sync with TensorBoard upstream:
#
# - //java/org/guildai/vulcanize
# - //components:vulcanize.bzl

package(default_visibility = ["//visibility:public"])

java_binary(
    name = "Vulcanize",
    srcs = ["Vulcanize.java"],
    jvm_flags = [
        "-Xss20m",  # JSCompiler needs big stacks for recursive parsing
        "-XX:+UseParallelGC",  # Best GC when app isn't latency sensitive
        "-Djava.util.logging.SimpleFormatter.format='%1$$tY-%1$$tm-%1$$td %1$$tH:%1$$tM:%1$$tS.%1$$tL %4$$-6s %5$$s%6$$s%n'",  # Less log spam
    ],
    deps = [
        "//java/org/jsoup/parser:HtmlTreeBuilder2",
        "@com_google_guava",
        "@com_google_protobuf_java",
        "@io_bazel_rules_closure//closure/compiler",
        "@io_bazel_rules_closure//java/io/bazel/rules/closure:webpath",
        "@io_bazel_rules_closure//java/io/bazel/rules/closure/webfiles:build_info_java_proto",
        "@io_bazel_rules_closure//java/org/jsoup/nodes",
        "@org_jsoup",
    ],
)

# These JS files are always taken into consideration by the Closure Compiler
# when vulcanizing, per vulcanize.bzl.
filegroup(
    name = "jslibs",
    srcs = [
        # Ordering probably matters
        "@com_google_javascript_closure_compiler_externs",
        "@com_google_javascript_closure_compiler_externs_polymer",
        "externs.js",
        "@com_google_javascript_closure_library//:closure/goog/base.js",
        "@com_google_javascript_closure_library//:closure/goog/deps.js",
    ],
)
