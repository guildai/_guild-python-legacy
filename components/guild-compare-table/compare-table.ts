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

namespace GuildCompareTable {

    export function fieldsDataSource(fields) {
        var sources = new Set();
        fields.forEach(function(field) {
            if (field.source) {
                sources.add(field.source);
            }
        });
        return Array.from(sources).join(",");
    }

    export function init(table, fields, options) {
        return jQuery(table).DataTable({
            data: [],
            rowId: "run.id",
            columns: columns(fields),
            order: [[2, 'desc']],
            scrollY: (options && options.height) || "360px",
            scrollCollapse: true,
            paging: false,
            language: {
                info: "_TOTAL_ runs",
                infoFiltered: " (filtered from _MAX_)",
                infoEmpty: "_TOTAL_ runs",
                search: "",
                searchPlaceholder: "Filter",
                zeroRecords: "Waiting for data"
            },
            dom: "<'row'<'col-12'f>>"
                + "<'row'<'col-12'tr>>"
                + "<'row'<'col-12'i>>"
        });
    }

    function columns(fields) {
        return baseCols().concat(fieldCols(fields));
    }

    function baseCols() {
        return [
            selectedCol(),
            statusCol(),
            timeCol(),
            modelCol()
        ];
    }

    function selectedCol() {
        return {
            title: "<guild-compare-table-select header></guild-compare-table-select>",
            data: null,
            orderable: false,
            width: "18px",
            render: {
                display: function(item) {
                    return tableSelect();
                }
            }
        }
    }

    function tableSelect() {
        return "<guild-compare-table-select></guild-compare-table-select>";
    }

    function statusCol() {
        return {
            title: statusTitle(),
            data: "status",
            width: "20px",
            render: {
                display: function(status) {
                    return statusIcon(status);
                },
                sort: "sort",
                filter: "label"
            }
        }
    }

    function statusTitle() {
        return "<span class='header-title status-title'></span>";
    }

    function statusIcon(status) {
        return "<fa-awesome class='" + status.iconClass + "'"
            + maybeSpinAttr(status.spin)
            + " icon='" + status.icon
            + "' size='22'></fa-awesome>"
            + "<paper-tooltip position='right'"
            + " animation-delay='250' offset='0'>"
            + status.label + "</paper-tooltip>";
    }

    function maybeSpinAttr(spin) {
        return spin ? " spin" : "";
    }

    function timeCol() {
        return {
            title: headerTitle("Time"),
            data: "time",
            orderSequence: ["desc", "asc"],
            width: "8em",
            render: {
                display: function(time, _type, row) {
                    return runLink(time.value, row.run);
                },
                sort: "sort",
                filter: "value"
            }
        }
    }

    function headerTitle(title) {
        return "<span class='header-title'>" + title + "</span>";
    }

    function runLink(val, run) {
        var link = "/train?run=" + run.id;
        return "<a href='" + link + "' class='date'>" + val + "</a>";
    }

    function modelCol() {
        return {
            title: headerTitle("Model"),
            data: "run",
            render: {
                display: "model",
                sort: "model",
                filter: "model"
            }
        }
    }

    function fieldCols(fields) {
        return fields.map(function(field, index) {
            return {
                title: headerTitle(field.label),
                data: "f" + index,
                orderSequence: ["desc", "asc"],
                type: fieldType(field),
                render: function(field, type) {
                    if (type == "sort") {
                        return field.sort;
                    } else {
                        return field.value;
                    }
                },
                render_: {
                    display: "value",
                    sort: "sort",
                    filter: "value"
                }
            }
        });
    }

    function fieldType(field) {
        // Infer numeric type by reduce function
        return field.reduce ? "num" : "string";
    }

    export function refresh(dt, data, fields) {
        var items = formatItems(data, fields);
        deleteMissingRows(dt, items);
        addOrUpdateRows(dt, items);
   }

    function formatItems(data, fields) {
        return data.map(function(item, index) {
            return Object.assign(
                itemBase(item, index),
                itemFields(item, fields));
        });
    }

    function itemBase(item, index) {
        return {
            run: item.run,
            time: formatTime(item.run.started),
            status: runStatus(item.run),
            index: index,
            selected: false
        }
    }

    function runStatus(run) {
        var status = GuildRun.runStatus(run);
        status.sort = statusSort(status);
        return status;
    }

    function statusSort(status) {
        var label = status.label;
        if (label == "Running") {
            return 0;
        } else if (label == "Completed") {
            return 1;
        } else if (label == "Terminated") {
            return 2;
        } else if (label == "Error") {
            return 3;
        } else {
            return 4;
        }
    }

    function formatTime(epoch) {
        return {
            value: GuildUtil.formatShortDate(new Date(epoch)),
            sort: epoch
        }
    }

    function itemFields(item, fieldDefs) {
        var fields = {}
        fieldDefs.forEach(function(field, index) {
            var data = item[field.source];
            var name = "f" + index;
            fields[name] = fieldValue(data, field);
        });
        return fields;
    }

    function fieldValue(data, field) {
        var raw = fieldRawValue(data, field);
        var sort = raw == undefined ? null: raw;
        var formatted = fieldFormattedValue(raw, field) || "";
        return {sort: sort, value: formatted}
    }

    function fieldRawValue(data, field) {
        if (field.attribute) {
            return data[field.attribute];
        } else if (field.reduce) {
            var reduce = GuildUtil.reduceFunctions[field.reduce];
            if (reduce) {
                var reduced = reduce(data);
                return reduced[Object.keys(reduced)[0]];
            }
        }
        return undefined;
    }

    function fieldFormattedValue(raw, field) {
        return field.format
            ? GuildUtil.tryFormat(raw, field.format)
            : raw;
    }

    function deleteMissingRows(dt, items) {
        var itemIds = itemIdLookup(items);
        var missing = [];
        dt.rows().every(function(index) {
            if (!itemIds.has(dt.row(index).data().run.id)) {
                missing.push(index);
            }
        });
        if (missing.length > 0) {
            dt.rows(missing).remove().draw();
        }
    }

    function itemIdLookup(items) {
        var ids = items.map(function(item) { return item.run.id; });
        return new Set(ids);
    }

    function addOrUpdateRows(dt, items) {
        var added = false;
        items.forEach(function(item, index) {
            var curRow = findRow(dt, item);
            if (curRow != null) {
                updateRow(dt, curRow, item);
            } else {
                addRow(dt, item);
                added = true;
            }
        });
        if (added) {
            dt.columns.adjust();
        }
    }

    function findRow(dt, target) {
        var row = dt.row("#" + target.run.id);
        return row.data() != undefined ? row : null;
    }

    function updateRow(dt, row, newItem) {
        var curItem = row.data();
        dt.columns().every(function(colIndex) {
            var property = dt.column(colIndex).dataSrc();
            var curVal = curItem[property];
            var newVal = newItem[property];
            if (itemValChanged(curVal, newVal)) {
                dt.cell(row, colIndex).data(newVal);
            }
        });
    }

    function itemValChanged(a, b) {
        return JSON.stringify(a) != JSON.stringify(b);
    }

    function rowCellChanged(index, curVal, newVal) {
        if (index == 0) {
            return curVal.status != newVal.status;
        } else {
            return curVal != newVal;
        }
    }

    function addRow(dt, item) {
        var row = dt.row.add(item);
        row.draw();
    }

    export function refreshRowsForSelected(dt) {
        dt.rows().every(function(index) {
            var tr = dt.row(index).node();
            var item = dt.row(index).data();
            var select = tr.querySelector("guild-compare-table-select");
            if (select.value == "true") {
                item.selected = true;
                $(tr).addClass("highlight");
            } else {
                item.selected = false;
                $(tr).removeClass("highlight");
            }
        });
    }

    export function refreshSelectHeader(dt) {
        var header = headerSelectForTable(dt);
        var selects = selectsForTable(dt);
        header.value = headerValueForSelects(selects);
    }

    function headerSelectForTable(dt) {
        return dt.table().header().querySelector("guild-compare-table-select");
    }

    function selectsForTable(dt) {
        return dt.table().body().querySelectorAll("guild-compare-table-select");
    }

    function headerValueForSelects(selects) {
        var first = null;
        for (var i = 0; i < selects.length; i++) {
            var cur = selects[i].value;
            if (first == null) {
                first = cur;
            } else if (first != cur) {
                return "mixed";
            }
        }
        return first || "false";
    }

    export function syncSelectsWithHeader(dt) {
        var header = headerSelectForTable(dt);
        var selects = selectsForTable(dt);
        selects.forEach(function(select) {
            select.value = header.value;
        });
    }

    export function deselectRemoved(dt) {
        var removed = removedItems(dt);
        var deselected = false;
        for (var i in removed) {
            var item = removed[i];
            if (item.selected) {
                deselect(dt, item);
                deselected = true;
            }
        }
        return deselected;
    }

    export function removedItems(dt) {
        return dt.rows({search: "removed"}).data().toArray();
    }

    export function deselect(dt, item) {
        tableSelectComponent(dt, item).value = "false";
    }

    function tableSelectComponent(dt, item) {
        var row = findRow(dt, item);
        return dt.cell(row, 0).node().firstChild;
    }

    export function runsChanged(a, b) {
        // Returns true if any of these are true:
        //
        // - length of a and b differ
        // - run ID for a[N] and b[N] differ
        // - run status for a[N] and b[N] differ
        //
        // This is an optimization based on our defintion of "change", which
        // is restricted to run status.
        //
        if (!a || !b || a.length != b.length) {
            return true;
        } else {
            for (var i = 0; i < a.length; i++) {
                var aRun = a[i];
                var bRun = b[i];
                if (aRun.id != bRun.id || aRun.status != bRun.status) {
                    return true;
                }
            }
            return false;
        }
    }
}
