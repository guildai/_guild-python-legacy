/* Copyright 2016-2017 TensorHub, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { formatShortDate } from "../guild-util/util.js";

export function runLabel(run) {
    var label = "";
    if (run.started) {
        var started = new Date(run.started);
        label += formatShortDate(started);
    }
    if (run.model) {
        if (label) {
            label += " - ";
        }
        label += run.model;
    }
    return label;
}

const runStatusRules = [
    [["running"],
     {label: "Running",
      iconClass: "icon running",
      icon:  "fa:circle-o-notch",
      spin: true}],
    [["stopped", 0],
     {label: "Completed",
      iconClass: "icon completed",
      icon:  "check-circle"}],
    [["stopped"],
     {label: "Error",
      iconClass: "icon error",
      icon:  "error"}],
    [["crashed"],
     {label: "Terminated",
      iconClass: "icon crashed",
      icon:  "cancel"}],
    [[],
     {label: "--",
      iconClass: "icon unknown",
      icon:  "help"}]
];

export function runStatus(run) {
    for (let rule of runStatusRules) {
        let status = rule[0];
        // Not sure why this requires a cast, but it appears to
        let statusParts = (<any[]>status).length;
        let attrs = rule[1];
        if ((statusParts == 0)
            || (statusParts == 1
                && status[0] == run.status)
            || (statusParts == 2
                && status[0] == run.status
                && status[1] == run.exit_status))
        {
            return attrs;
        }
    }
    throw "unreachable"; // rules must have catch-all
}

export function runForId(runId, runs) {
    return runs.find(function(run) {
        return run.id == runId;
    });
}

export function isRunning(run) {
    return run && run.status == "running";
}
