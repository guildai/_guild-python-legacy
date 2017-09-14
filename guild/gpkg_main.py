import guild.cli
import guild.main_impl

import guild.info_cmd
import guild.search_cmd
import guild.sources_cmd
import guild.sync_cmd

def main():
    guild.main_impl.set_git_commit()
    guild.cli.main(
        "gpkg",
        "Guild AI Packaging command line interface.",
        [
            guild.info_cmd,
            guild.search_cmd,
            guild.sources_cmd,
            guild.sync_cmd,
        ])

if __name__ == "__main__":
    main()
