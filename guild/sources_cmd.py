import guild.cli
import guild.user

def main(args):
    if args.sources_command is None:
        _list_sources(args)
    elif args.sources_command == "add":
        _add_source(args)
        _maybe_sync(args)
    elif args.sources_command == "remove" or args.sources_command == "rm":
        _delete_source(args)
        _maybe_sync(args)
    else:
        _unknown_command_error(args.sources_command)

def _list_sources(args):
    for source in guild.user.read_config("package-sources", []):
        _print_source(source, args)

def _print_source(source, args):
    if args.verbose:
        print("%s\t%s" % (source.get("name", "-"), source.get("url", "-")))
    else:
        print(source.get("name", "-"))

def _add_source(args):
    if not args.name:
        guild.cli.error("missing required source NAME")
    if not args.url:
        guild.cli.error("missing required source URL")
    sources = guild.user.read_config("package-sources", [])
    _verify_source_not_exists(args.name, sources)
    sources.append({
        "name": args.name,
        "url": args.url
    })
    guild.user.write_config("package-sources", sources)

def _verify_source_not_exists(name, sources):
    for source in sources:
        if source.get("name") == name:
            _source_exists_error(name)

def _source_exists_error(name):
    guild.cli.error("source '%s' already exists" % name)

def _maybe_sync(args):
    if not args.nosync:
        _sync()

def _sync():
    import guild.sync_cmd
    guild.sync_cmd.main([])

def _delete_source(args):
    if not args.name:
        guild.cli.error("missing required source NAME")
    sources = guild.user.read_config("package-sources", [])
    for source in sources:
        if source.get("name") == args.name:
            sources.remove(source)
            break
    else:
        _source_not_exists_error(args.name)
    guild.user.write_config("package-sources", sources)

def _source_not_exists_error(name):
    guild.cli.error("source '%s' does not exist" % name)

def _unknown_command_error(cmd):
    guild.cli.error(
        "unknown runs command '%s'\n"
        "Try 'guild sources --help' for a list of commands"
        % cmd)
