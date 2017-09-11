export function selectedRun(runs, route) {
    var runId = route.__queryParams.run;
    if (runId) {
        return parseInt(runId, 10) || null;
    } else {
        return runs.length > 0 ? runs[0].id : null;
    }
}

export function applyRunParam(runId, params) {
    var base = Object.assign({}, params);
    return Object.assign(base, {"run": runId.toString()});
}

export function deleteRunParam (params) {
    var base = Object.assign({}, params);
    delete base["run"];
    return base;
}
