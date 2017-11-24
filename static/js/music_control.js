$.widget("custom.music_control", {
    options: {
        sound_file: "",
        progresser: "",
        onload: {}
    },

    _create: function() {
        var self = this;
        this.sound = new Howl({
            src: [this.options.sound_file],
            format: "mp3",
            onload: function() {
                self.options.onload(self);
                self.create_slider(this.duration() * 1000);
            },
            onend: function() {
                self.pause_progress();
            }
        });
        this.create_buttons();
        $("#music_control").append("<p id='time'></p>");

    },

    create_slider: function(duration) {
        var self = this;
        $("#slider").slider({
            min: 0,
            max: duration,
            step: 0.001,
            stop: function(event, ui) {
                self.sound.seek(ui.value / 1000);
                self.set_slider(self.sound.seek());
                if (self.sound.playing()) {
                    self.start_progress();
                }
            },
            slide: function(event, ui) {
                self.visualizer.visualization('seek', ui.value / 1000);
                self.set_time(ui.value);
            },
            start: function() {
                self.pause_progress();
            }
        });
    },

    create_buttons: function() {

        $("#music_control").append("<div class='controls'>" +
            "<button id='play'>Play</button>" +
            "<button id='pause'>Pause</button>" +
            "<button id='stop'>Stop</button>" +
            "<div id='slider'></div>");

        var self = this;
        $("#play").on("click", function() {
            if (!self.sound.playing()) {
                self.sound.play();
                self.start_progress();
            }
        });

        $("#pause").on("click", function() {
            self.sound.pause();
            self.visualizer.visualization('pause');
            self.pause_progress();
        });

        $("#stop").on("click", function() {
            self.sound.stop();
            self.visualizer.visualization('stop');
            self.set_slider(0);
        });
    },

    start_progress: function() {
        var self = this;
        this.options.progresser = setInterval(function() {
            var milli = self.sound.seek() * 1000;
            self.set_slider(milli);
            self.visualizer.visualization('seek', self.sound.seek());
            self.set_time(milli);
        }, 1);
    },

    pause_progress: function() {
        clearInterval(this.options.progresser);
    },

    set_slider: function(value) {
        $("#slider").slider("option", "value", value);
    },

    set_time: function(value) {
        $("#time").html(this.format_time(value));
    },

    format_time: function(value) {
        var milli = (value%1000).toFixed(0);
        var seconds = (value/1000).toFixed(0);
        return seconds + ":" + milli;
    },

    get_song_length: function() {
        return this.sound.duration();
    },

    set_visualizer: function(vis) {
        this.visualizer = vis
    },

    set_rate: function(rate) {
         this.sound.rate(rate);
    }
});