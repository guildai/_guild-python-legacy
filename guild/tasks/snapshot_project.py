import subprocess

import guild.app
import guild.log
import guild.opdir

def start(op, _stop, section):
    sources = _sources_for_section(section)
    if sources:
        script = guild.app.script("snapshot-project")
        project_dir = section.project.dir
        guild_dir = guild.opdir.guild_dir(op.opdir)
        args = [script, project_dir, guild_dir, sources]
        guild.log.debug("project sources: %s", sources)
        try:
            subprocess.check_output(args)
        except subprocess.CalledProcessError:
            guild.log.exception("snapshoting project")

def _sources_for_section(section):
    return section.attr("sources") or section.project.attr("sources")
