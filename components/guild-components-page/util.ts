import { section as projectSection } from "../guild-project/project.js";

export function viewForRun(project, run, scope) {
    return projectSection(project, "views", scope);
}

export function viewComponents(view, type, project) {
    let refs = view[type] || [];
    let comps = [];
    for (let i = 0; i < refs.length; i++) {
        let cdef = projectSection(project, "components", refs[i]);
        if (cdef) {
            comps.push(cdef);
        }
    }
    return comps;
}
