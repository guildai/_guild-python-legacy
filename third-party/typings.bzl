load("@io_bazel_rules_closure//closure:defs.bzl", "filegroup_external")

def guild_typings_workspace():

  filegroup_external(
      name = "org_definitelytyped_types_d3_time_format",
      licenses = ["notice"],  # MIT
      sha256_urls = {
          "1c99321e968c6b8b8d9fdd07d73703504987abbdb6bfca85eaf22f6baa014d26": [
              "https://raw.githubusercontent.com/DefinitelyTyped/DefinitelyTyped/38894f063d8711edebf1b846b34ba55d59a10577/types/d3-time-format/index.d.ts",  # 2017-09-03
          ],
      },
  )

  filegroup_external(
      name = "org_definitelytyped_types_numeral",
      licenses = ["notice"],  # MIT
      sha256_urls = {
          "fd3a508f39ccfee69b959cbea63a2223bb373962104fa4c2b855b6e9dc85140b": [
              "https://raw.githubusercontent.com/DefinitelyTyped/DefinitelyTyped/38894f063d8711edebf1b846b34ba55d59a10577/types/numeral/index.d.ts",  # 2017-09-03
          ],
      },
  )
  
