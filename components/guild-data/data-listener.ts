import { tryFormat } from "../guild-util/util.js";
import { reduceFunctions } from "../guild-util/reduce.js";
import { scheduleFetch } from "./data.js";

export let DataListener = {

    properties: {
        dataSource: String,
        dataFetchInterval: {
            type: Number,
            observer: "dataFetchIntervalChanged"
        },
        dataReduce: String,
        dataFormat: String,
        dataPrefix: {
            type: String,
            value: "/data/"
        },
        active: {
            type: Boolean,
            value: true,
            observer: 'activeChanged'
        },
        pendingFetch: {
            type: Object,
            value: null
        }
    },

    observers: [
        "maybeFetch(dataSource, active)"
    ],

    maybeFetch: function(source, active) {
        if (source && active) {
            this.scheduleFetch(0);
        }
    },

    scheduleFetch: function(whenSeconds) {
        if (this.dataSource && this.active) {
            var url = this.dataFetchUrl();
            var handler = this.handleFetchResult.bind(this);
            this.cancelPendingFetch();
            this.pendingFetch =
                scheduleFetch(url, handler, whenSeconds * 1000);
        }
    },

    dataFetchUrl: function() {
        return this.dataPrefix + this.dataSource;
    },

    handleFetchResult: function(result) {
        this.cancelPendingFetch();
        if (result != null) {
            var data = this.maybeReduce(result);
            this.handleData.bind(this)(data);
        }
        this.maybeScheduleNextFetch();
    },

    cancelPendingFetch: function() {
        if (this.pendingFetch) {
            window.clearTimeout(this.pendingFetch);
            this.pendingFetch = null;
        }
    },

    maybeScheduleNextFetch: function() {
        if (this.dataFetchInterval > 0 && !this.pendingFetch) {
            this.scheduleFetch(this.dataFetchInterval);
        }
    },

    maybeReduce: function(data) {
        var reduce = reduceFunctions[this.dataReduce];
        return reduce ? reduce(data) : data;
    },

    handleData: function(data) {
        // stub to be overridden by host
    },

    formatData: function(data, defaultValue) {
        var val = this.dataValue(data);
        if (val != undefined) {
            return tryFormat(val, this.dataFormat);
        } else {
            return defaultValue;
        }
    },

    dataValue: function(data) {
        if (typeof data === "object" && data != null) {
            return data[Object.keys(data)[0]];
        } else {
            return data;
        }
    },

    dataFetchIntervalChanged: function(interval, old) {
        if (interval > 0) {
            this.maybeFetch(this.dataSource, this.active);
        }
    },

    activeChanged: function(val, old) {
        if (old !== undefined) {
            this.cancelPendingFetch();
            if (val) {
                this.scheduleFetch(0);
            }
        }
    }
}
