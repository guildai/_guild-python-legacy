class ProjectView(object):

    def __init__(self, project, opts):
        self._runs_dir = guild.project_util.runs_dir_for_project(project)

    def runs(self):
        pass
