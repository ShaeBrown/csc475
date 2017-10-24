$.widget("custom.visualization", {
    options: {
        drum_data: {},
        width: 1000,
        height: 100,
        song_length: 18000,
        drum_props: {
            "Snare drum": {
                color: "green",
                radius: 10
            },
            "Bass drum": {
                color: "blue",
                radius: 20
            }
        }
    },

    _create: function() {

        this.svgContainer = d3.select('body')
            .append('svg')
            .attr('class', 'visualization')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

       this.svgContainer.append("line")
            .attr("y1", 0)
            .attr("y2", this.options.height)
            .attr("x1", 0)
            .attr("x2", 1)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

        var drum_circles = this._get_circle_data(this.options.drum_data);
        this.circles = this.svgContainer.append("g").selectAll("circle")
            .data(drum_circles)
            .enter()
            .append("circle");

        this.circles_attr = this.circles
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
            .attr("r", function(d) { return d.radius; })
            .attr("class", function(d) {return d.c; })
            .style("fill", function(d) { return d.color; });

        var scale = d3.scaleLinear()
            .domain([0, this.options.song_length])
            .range([0, this.options.song_length]);

        var xAxis = d3.axisBottom(scale)
            .ticks(18)
            .tickFormat(function(d) {
                var minutes = Math.floor(d / 60000);
                var seconds = ((d % 60000) / 1000).toFixed(0);
                return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
            });

        this.axis = this.svgContainer.append("g").call(xAxis);
    },

    _get_circle_data: function(drum_events) {
        var jsonCircles = [];
        Object.keys(drum_events).forEach(function(drum_type) {
            drum_events[drum_type].forEach(function(time) {
                var radius = this.options.drum_props[drum_type].radius;
                var color = this.options.drum_props[drum_type].color;
                jsonCircles.push({
                    "x": time * 1000,
                    "y": this.options.height / 2,
                    "radius": radius,
                    "color": color,
                    "c": drum_type
                })
            }, this);
        }, this);
        return jsonCircles;
    },

    pause: function() {
        this.circles.transition();
        this.axis.transition();
    },

    seek: function(milliseconds) {
        this.circles
            .transition()
            .duration(0.1)
            .attr("transform", "translate(" + -milliseconds + ")");

        this.axis
            .transition()
            .duration(0.1)
            .attr("transform", "translate(" + -milliseconds + ")");
    },

    stop: function() {
        this.seek(0);
    },
});