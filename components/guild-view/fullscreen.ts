
export let FullscreenBehavior = {

    properties: {
        fullscreen: {
            type: Boolean,
            value: false,
            notify: true,
            observer: 'fullscreenChanged'
        },
        fullscreenIcon: {
            type: String,
            computed: 'computeFullscreenIcon(fullscreen)'
        },
        fullscreenContent: {
            type: Object,
            value: function() {
                return this;
            }
        },
        fullscreenNotifyTarget: {
            type: Object,
            value: function() {
                return this;
            }
        }
    },

    listeners: {
        'fullscreen-canceled': 'handleFullscreenCanceled'
    },

    computeFullscreenIcon: function(fullscreen) {
        return fullscreen ? "fullscreen-exit" : "fullscreen";
    },

    toggleFullscreen: function() {
        this.fullscreen = !this.fullscreen;
    },

    fullscreenChanged: function(val, old) {
        if (old == undefined) return;
        if (val) {
            this.onFullscreen();
            this.fireFullscreenEvent("fullscreen");
        } else {
            this.onFullscreenExit();
            this.fireFullscreenEvent("fullscreen-exit");
        }
    },

    fireFullscreenEvent: function(name) {
        var event = {
            content: this.fullscreenContent,
            notifyTarget: this.fullscreenNotifyTarget
        };
        this.fire(name, event);
    },

    onFullscreen: function() {
        // To be overridden
    },

    onFullscreenExit: function() {
        // To be overridden
    },

    handleFullscreenCanceled: function(e) {
        this.fullscreen = false;
    }
}

export let FullscreenHost = {

    properties: {
        fullscreenNotifyTarget: Object,
        notifyingFullscreenCanceled: {
            type: Boolean,
            value: false
        }
    },

    listeners: {
        'fullscreen': 'handleFullscreen',
        'fullscreen-exit': 'handleFullscreenExit',
        'fullscreen-canceled': 'handleFullscreenCanceled'
    },

    handleFullscreen: function(e) {
        var fullscreen = this.$$("guild-view-fullscreen");
        fullscreen.content = e.detail.content;
        this.fullscreenNotifyTarget = e.detail.notifyTarget;
        fullscreen.open();
    },

    handleFullscreenExit: function(e) {
        var fullscreen = this.$$("guild-view-fullscreen");
        fullscreen.cancel();
    },

    handleFullscreenCanceled: function(e) {
        if (!this.notifyingFullscreenCanceled
            && this.fullscreenNotifyTarget) {
            this.notifyingFullscreenCanceled = true;
            this.fullscreenNotifyTarget.fire(e.type);
            this.notifyingFullscreenCanceled = false;
        }
    }
}
