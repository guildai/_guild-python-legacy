import os
import yaml

class Project(object):

    def __init__(self, data, path):
        self.data = data
        self.path = path
        self.dir = os.path.dirname(path)

    def attr(self, name):
        return self.data.get(name)

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

class Section(object):

    def __init__(self, path, data, project):
        self.path = path
        self.data = data
        self.project = project

    def attr(self, key):
        return self.data.get(key)

def from_dir(path, name="guild.yml"):
    return from_file(os.path.join(path, name))

def from_file(path):
    with open(path, "r") as f:
        parsed = yaml.load(f)
    return Project(parsed, path)
