import { section as projectSection } from "../guild-project/project.js";

export function projectSeries(project, run) {
    // TODO use scope to resolve series
    return projectSection(project, "train-series");
}

export function extraSeries(project) {
    var series = [];
    var componentDef = projectSection(project, "components", "series");
    if (componentDef) {
        var names = componentDef.extra_series_templates || [];
        for (var i = 0; i < names.length; i++) {
            var template = projectSection(
                project, "templates", names[i]);
            if (template) {
                series.push(template);
            }
        }
    }
    return series;
}
