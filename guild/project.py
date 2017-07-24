import os
import yaml

class Project(object):

    def __init__(self, data, path):
        self.data = data
        self.path = path
        self.dir = os.path.dirname(path)
        self.command_line_flags = []
        self.command_line_profiles = []

    def attr(self, name, default=None):
        return self.data.get(name, default)

    def sections(self, heading):
        sections = self.data.get(heading)
        keys = sections.keys()
        keys.sort()
        return [Section([heading, key], sections[key], self) for key in keys]

    def section(self, heading, key):
        data = self.data.get(heading, {}).get(key)
        if data:
            return Section([heading, key], data, self)
        else:
            return None

    def default_section(self, heading):
        for s in self.sections(heading):
            if s.attr("default") is True:
                return s
        return None

    def flags(self):
        return self.data.get("flags", {})

    def all_flags(self):
        return merge_flags(
            self.command_line_flags,
            resolve_profile_flags(self),
            self.flags())

class Section(object):

    def __init__(self, path, data, project):
        self.path = path
        self.data = data
        self.project = project

    def attr(self, key, default=None):
        return self.data.get(key, default)

    def flags(self):
        return self.attr("flags", {})

    def all_flags(self):
        return merge_flags(
            self.project.command_line_flags,
            resolve_profile_flags(self.project),
            self.flags(),
            self.project.flags())

def merge_flags(*list_of_flags):
    merged = []
    for flags in list_of_flags:
        for name, val in iter_flags(flags):
            if not has_flag(name, merged):
                merged.append((name, val))
    return merged

def iter_flags(flags):
    try:
        return flags.items()
    except AttributeError:
        return flags

def resolve_profile_flags(project):
    resolved = []
    for profile_name in project.command_line_profiles:
        profile = project.section("profiles", profile_name)
        if profile:
            resolved = merge_flags(profile.data, resolved)
    return resolved

def has_flag(name, flags):
    for flag_name, _ in flags:
        if flag_name == name:
            return True
    return False

def from_dir(path, name="guild.yml"):
    return from_file(os.path.join(path, name))

def from_file(path):
    with open(path, "r") as f:
        parsed = yaml.load(f)
    return Project(parsed, path)
