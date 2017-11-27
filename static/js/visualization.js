$.widget("custom.visualization", {
    options: {
        drum_data: {},
        widget_height: 100,
        song_length: 18,
        zoom_rate: 0.5,
        drum_props: {
            "Snare drum": {
                color: "green",
                radius: 10,
                height: 30
            },
            "Bass drum": {
                color: "blue",
                radius: 10,
                height: 50
            },
            "Hi-hat closed": {
                color: "pink",
                radius: 10,
                height: 70
            },
            "Hi-hat open": {
                color: "orange",
                radius: 10,
                height: 90
            }
        }
    },

    _create: function() {
        this.width = this.options.song_length * this.options.zoom_rate * 1000;
        this.svgContainer = d3.select('#visualization')
            .append('svg')
            .attr('class', 'visualization')
            .attr('width', this.width)
            .attr('height', this.options.widget_height);

        this.svgContainer.append("line")
            .attr("y1", 0)
            .attr("y2", this.options.widget_height)
            .attr("x1", 0)
            .attr("x2", 1)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

        this.scale = d3.scaleLinear()
            .domain([0, this.options.song_length])
            .range([0, this.width]);

        var drum_circles = this._get_circle_data(this.options.drum_data);
        this.circles = this.svgContainer.append("g").selectAll("circle")
            .data(drum_circles)
            .enter()
            .append("circle");

        this.circles_attr = this.circles
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
            .attr("r", function(d) { return d.radius; })
            .attr("class", function(d) { return d.c; })
            .style("fill", function(d) { return d.color; });

        var xAxis = d3.axisBottom(this.scale)
            .ticks(this.options.song_length * this.options.zoom_rate * 100)
            .tickSize(10)
            .tickFormat(function(d) {
                var milli = (d * 1000 % 1000).toFixed(0);
                var seconds = d.toFixed(0);
                if (milli == 0) {
                    return seconds + "s";
                } else if (milli % 100 == 0) {
                    return milli;
                } else {
                    "";
                }
            });

        this.axis = this.svgContainer.append("g").call(xAxis);
        d3.selectAll(".tick line")
            .attr("y2", function(d) {
                var milli = (d * 1000 % 1000).toFixed(0);
                if (milli == 0) {
                    return 12;
                } else if (milli % 100 == 0) {
                    return 10;
                } else if  (milli % 10 == 0) {
                    return 5;
                } else {
                    return 2;
                }
            });
    },

    _get_circle_data: function(drum_events) {
        var jsonCircles = [];
        Object.keys(drum_events).forEach(function(drum_type) {
            drum_events[drum_type].forEach(function(time) {
                var radius = this.options.drum_props[drum_type].radius;
                var color = this.options.drum_props[drum_type].color;
                var height = this.options.drum_props[drum_type].height;
                jsonCircles.push({
                    "x": this.scale(time),
                    "y": height,
                    "radius": radius,
                    "color": color,
                    "c": drum_type
                });
            }, this);
        }, this);
        return jsonCircles;
    },

    pause: function() {
        this.circles.transition();
        this.axis.transition();
    },

    seek: function(seconds) {
        this.circles
            .transition()
            .duration(0.1)
            .attr("transform", "translate(" + -this.scale(seconds) + ")");

        this.axis
            .transition()
            .duration(0.1)
            .attr("transform", "translate(" + -this.scale(seconds) + ")");
    },

    stop: function() {
        this.seek(0);
    },
});