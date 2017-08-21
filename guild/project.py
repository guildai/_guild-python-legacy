import os
import yaml

class Project(object):

    def __init__(self, data, source=None, dir=None, annotation=None):
        self.data = data
        self.source = source
        self.dir = dir
        self.annotation = annotation
        self.command_line_flags = []
        self.command_line_profiles = []

    def attr(self, name, default=None):
        return self.data.get(name, default)

    def sections(self, heading):
        sections = self.data.get(heading, {})
        keys = list(sections.keys())
        keys.sort()
        return [Section([heading, key], sections[key], self) for key in keys]

    def section(self, heading, key):
        data = self.data.get(heading, {}).get(key)
        if data:
            return Section([heading, key], data, self)
        else:
            return None

    def default_section(self, heading):
        sections = self.sections(heading)
        if len(sections) == 1:
            return sections[0]
        else:
            for s in self.sections(heading):
                if s.attr("default") is True:
                    return s
            return None

    def flags(self):
        return self.data.get("flags", {})

    def all_flags(self):
        return _merge_flags(
            self.command_line_flags,
            _resolve_profile_flags(self),
            self.flags())

    def reload(self):
        if project.source:
            self.data = _load_data(project.source)

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
        return _merge_flags(
            self.project.command_line_flags,
            _resolve_profile_flags(self.project),
            self.flags(),
            self.project.flags())

def _merge_flags(*list_of_flags):
    merged = []
    for flags in list_of_flags:
        for name, val in _iter_flags(flags):
            if not _has_flag(name, merged):
                merged.append((name, val))
    return merged

def _iter_flags(flags):
    try:
        return flags.items()
    except AttributeError:
        return flags

def _resolve_profile_flags(project):
    resolved = []
    for profile_name in project.command_line_profiles:
        profile = project.section("profiles", profile_name)
        if profile:
            resolved = _merge_flags(profile.data, resolved)
    return resolved

def _has_flag(name, flags):
    for flag_name, _ in flags:
        if flag_name == name:
            return True
    return False

def from_dir(path, name="guild.yml"):
    return from_file(os.path.join(path, name))

def from_file(path):
    return Project(_load_data(path), path, os.path.dirname(path))

def _load_data(path):
    with open(path, "r") as f:
        return yaml.load(f)

def from_string(s, path="__str__"):
    return Project(yaml.load(s), path)

def copy_with_new_data(project, data):
    return Project(
        data,
        project.source,
        project.dir,
        project.annotation)
