import guild.cli
import guild.main_impl

import guild.check_cmd
import guild.evaluate_cmd
import guild.prepare_cmd
import guild.project_cmd
import guild.query_cmd
import guild.repos_cmd
import guild.runs_cmd
import guild.search_cmd
import guild.sync_cmd
import guild.train_cmd
import guild.view_cmd

def main():
    guild.main_impl.set_git_commit()
    guild.cli.main(
        "guild",
        "Guild AI command line interface.",
        [
            guild.check_cmd,
            guild.evaluate_cmd,
            guild.prepare_cmd,
            guild.project_cmd,
            guild.query_cmd,
            guild.runs_cmd,
            guild.train_cmd,
            guild.view_cmd,
        ])

if __name__ == "__main__":
    main()
