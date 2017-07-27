import subprocess

import guild

def start(op, section):
    sources = _sources_for_section(section)
    if sources:
        script = guild.app.script("snapshot-project")
        project_dir = section.project.dir
        guild_dir = guild.opdir.guild_dir(op.opdir)
        args = [script, project_dir, guild_dir, sources]
        try:
            subprocess.check_output(args)
        except subprocess.CalledProcessError as e:
            guild.log.error(e)

def _sources_for_section(section):
    return section.attr("sources") or section.project.attr("sources")
