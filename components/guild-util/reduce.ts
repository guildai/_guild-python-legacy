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

namespace guild.util {

    export function last_5_average(data) {
        return mapSeries(function(series) {
            return seriesAverage(series.slice(-5));
        }, data);
    }

    export function average(data) {
        return mapSeries(function(series) {
            return seriesAverage(series);
        }, data);
    }

    export function last(data) {
        return mapSeries(function(series) {
            return seriesLast(series);
        }, data);
    }

    export function steps(data) {
        return mapSeries(function(series) {
            return seriesSteps(series);
        }, data);
    }

    export function steps0(data) {
        return mapSeries(function(series) {
            return seriesSteps0(series);
        }, data);
    }

    export function duration(data) {
        return mapSeries(function(series) {
            return seriesDuration(series);
        }, data);
    }

    export function mapSeries(f, data) {
        var result = {};
        for (var name in data) {
            var series = data[name];
            result[name] = series ? f(series) : undefined;
        }
        return result;
    }

    export function seriesAverage(series) {
        if (!series) {
            return undefined;
        }
        var total = 0;
        for(var i in series) {
            total += series[i][2];
        }
        return total / series.length;
    }

    export function seriesLast(series) {
        if (!series) {
            return undefined;
        }
        return series[series.length - 1][2];
    }

    export function seriesSteps(series) {
        if (!series) {
            return 0;
        }
        var interval = series.length == 1 ? 1 : series[1][1] - series[0][1];
        return series[series.length - 1][1] + interval;
    }

    export function seriesSteps0(series) {
        if (!series) {
            return 0;
        }
        return series[series.length - 1][1];
    }

    export function seriesDuration(series) {
        if (!series || series.length < 2) {
            return null;
        }
        return (series[series.length - 1][0] - series[0][0]) / 1000;
    }

    export const reduceFunctions = {
        "last_5_average": last_5_average,
        "average": average,
        "last": last,
        "steps": steps,
        "steps0": steps0,
        "duration": duration
    }
}
