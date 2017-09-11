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

const SHORT_DATE_FORMAT = d3.timeFormat("%b %d %H:%M:%S");

export function tryFormat(value, format) {
    if (value != null && value != undefined && value == value) {
        try {
            return formatValue(value, format);
        } catch (err) {
            console.error(err);
            return value;
        }
    } else {
        return value;
    }
}

export function formatValue(value, format) {
    var split = splitFormatAndSuffix(format);
    var formatted;
    if (split.format.endsWith("e")) {
        formatted = formatExponential(value, split.format.slice(0, -1));
    } else {
        formatted = numeral(value).format(split.format);
    }
    return formatted + split.suffix;

}

function formatExponential(value, format) {
    var match = /0\.(0+)/.exec(format);
    if (match) {
        return value.toExponential(match[1].length);
    } else {
        return value.toExponential();
    }
}

function splitFormatAndSuffix(format) {
    // Guild specific additions to numeral formatting support
    var suffixes = [" ms"];
    for (var i in suffixes) {
        var suffix = suffixes[i];
        if (format.endsWith(suffix)) {
            return {
                format: format.substring(0, format.length - suffix.length),
                suffix: suffix
            };
        }
    }
    return {
        format: format,
        suffix: ""
    };
}

export function formatShortDate (date) {
    return SHORT_DATE_FORMAT(date);
}
