import guild.cli
import guild.cmd_support
# Avoid expensive imports here

def add_parser(subparsers):
    p = guild.cmd_support.add_parser(
        subparsers,
        "repos", "manage package repositories",
        """With no arguments, prints a list of repositories.

        Use 'add' to add a new repository. When adding a repository,
        specify a full Git repository repository URL or a path
        consisting of the pattern ACCOUNT/REPO, where ACCOUNT is a
        GitHub account and REPO is a Guild package repository. For
        example 'guild repos add guild guildai/packages' will add a
        repository named 'guild' with a source URL of the
        'guildai/packages' GitHub repository.

        Use 'remove' (or 'rm') to delete a repository.
        """)
    p.add_argument(
        "repos_command",
        help="optional command: add, remove (or rm)",
        metavar="COMMAND",
        nargs="?")
    p.add_argument(
        "name",
        help="repo name to add or delete",
        metavar="NAME",
        nargs="?")
    p.add_argument(
        "url",
        help="repo URL to add",
        metavar="URL",
        nargs="?")
    p.add_argument(
        "-s", "--sync",
        help="synchronize with repos after adding or deleting",
        action="store_true")
    p.add_argument(
        "-v", "--verbose",
        help="show repository details when printing a list",
        action="store_true")
    p.set_defaults(func=main)

def main(args):
    if args.repos_command is None:
        _list_repos(args)
    elif args.repos_command == "add":
        _add_repo(args)
    elif args.repos_command == "remove" or args.repos_command == "rm":
        _delete_repo(args)
    else:
        _unknown_command_error(args.repos_command)

def _list_repos(args):
    import guild.user
    for repo in guild.user.read_config("repos", []):
        _print_repo(repo, args)

def _print_repo(repo, args):
    if args.verbose:
        print("%s\t%s" % (repo.get("name", "-"), repo.get("url", "-")))
    else:
        print(repo.get("name", "-"))

def _add_repo(args):
    import guild.user
    if not args.name:
        guild.cli.error("missing required repo NAME")
    if not args.url:
        guild.cli.error("missing required repo URL")
    repos = guild.user.read_config("repos", [])
    _verify_repo_not_exists(args.name, repos)
    repos.append({
        "name": args.name,
        "url": args.url
    })
    guild.user.write_config("repos", repos)
    guild.cli.out("repo '%s' added", args.name)
    _maybe_sync(args)

def _verify_repo_not_exists(name, repos):
    for repo in repos:
        if repo.get("name") == name:
            _repo_exists_error(name)

def _repo_exists_error(name):
    guild.cli.error("repo '%s' already exists" % name)

def _maybe_sync(args):
    if args.sync:
        _sync()
    else:
        guild.cli.out(
            "Run 'guild sync' to synchronize with your repos before "
            "searching or installing packages.")

def _sync():
    print("TODO: run sync")

def _delete_repo(args):
    import guild.user
    if not args.name:
        guild.cli.error("missing required repo NAME")
    repos = guild.user.read_config("repos", [])
    for repo in repos:
        if repo.get("name") == args.name:
            repos.remove(repo)
            break
    else:
        _repo_not_exists_error(args.name)
    guild.user.write_config("repos", repos)
    guild.cli.out("repo '%s' deleted", args.name)
    _maybe_sync(args)
def _repo_not_exists_error(name):
    guild.cli.error("repo '%s' does not exist" % name)

def _unknown_command_error(cmd):
    guild.cli.error(
        "unknown runs command '%s'\n"
        "Try 'guild repos --help' for a list of commands"
        % cmd)
