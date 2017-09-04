load("@io_bazel_rules_closure//closure:defs.bzl", "filegroup_external")

def guild_typings_workspace():

  filegroup_external(
      name = "org_definitelytyped_d3_time_format",
      licenses = ["notice"],  # MIT
      sha256_urls = {
          "1c99321e968c6b8b8d9fdd07d73703504987abbdb6bfca85eaf22f6baa014d26": [
              "https://raw.githubusercontent.com/DefinitelyTyped/DefinitelyTyped/38894f063d8711edebf1b846b34ba55d59a10577/types/d3-time-format/index.d.ts",  # 2017-09-03
          ],
      },
  )

  filegroup_external(
      name = "org_definitelytyped_numeral",
      licenses = ["notice"],  # MIT
      sha256_urls = {
          "fd3a508f39ccfee69b959cbea63a2223bb373962104fa4c2b855b6e9dc85140b": [
              "https://raw.githubusercontent.com/DefinitelyTyped/DefinitelyTyped/38894f063d8711edebf1b846b34ba55d59a10577/types/numeral/index.d.ts",  # 2017-09-03
          ],
      },
  )
  
  filegroup_external(
      name = "org_definitelytyped_jquery",
      licenses = ["notice"],  # MIT
      sha256_urls = {
          "f55d9f693b58bc720889de5b0e4756ff44571b3ae4165b7a17ab6acfb7b193ec": [
              "https://raw.githubusercontent.com/DefinitelyTyped/DefinitelyTyped/38894f063d8711edebf1b846b34ba55d59a10577/types/jquery/index.d.ts",  # 2017-09-03
          ],
      },
  )
  
  filegroup_external(
      name = "org_definitelytyped_datatables",
      licenses = ["notice"],  # MIT
      sha256_urls = {
          "5e870cabc182744ac53d9391af037dbdb0b02c06e57217b7bf5392285ed737f4": [
              "https://raw.githubusercontent.com/DefinitelyTyped/DefinitelyTyped/38894f063d8711edebf1b846b34ba55d59a10577/types/datatables.net/index.d.ts",  # 2017-09-03
          ],
      },
  )
  
