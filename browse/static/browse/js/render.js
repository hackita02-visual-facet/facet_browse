/**
 * Created by azk on 15/12/15.
 */

"use strict";

var facetVis = (function () {

    var vis = {
        render_facet: function(label,data,selector) {
                if (label == "creationdate") {
                    render_creationdate(data, selector)
                } else {
                    render_treemap(data, selector)
                }
        },
        render_facets: function(all_facets,num_render,selector,ranks) {
            ranks = (typeof ranks === 'undefined') ? this.rank_facets(all_facets):ranks;

            if (ranks.length < num_render) {
                num_render = ranks.length
            }

            var rendered = 0;
            for (var i = 0;i < ranks.length; i++) {

                if (rendered == num_render) {
                    break;
                }

                if (all_facets[ranks[i]].length < 3) {
                    continue;
                }

                $(selector).append("<h4>" + facet_pretty_names[ranks[i]] + "</h4>");
                var _id = "facet" + i;

                var _div = $("<div id='" + _id + "'></div>" );
                $(selector).append(_div)
                this.render_facet(ranks[i],all_facets[ranks[i]],"#" + _id)
                rendered ++;
            }
        },
        rank_facets: function(all_facets,total_hits) {

            var ranks  =  _.intersection( _.keys(facet_pretty_names),_.keys(all_facets));
            console.log(ranks);
            return ranks
        }

    };

    function render_bar(data,selector) {
        var _id = $(selector).attr("id")+"_svg";
        console.log(_id)
        var svg = $("<svg id='" + _id + "' style='height:500px'></svg>" )
        $(selector).append(svg);
        selector = "#" + _id;

        //Pick the 10 most populous years
        data = _.sortBy(data,function(o) { return -o.value ;}).slice(0,10);
        //Now sort by year
        data = _.sortBy(data,"label");


        nv.addGraph(function () {
            var chart = nv.models.discreteBarChart()
                .x(function (d) {
                    return d.label
                })    //Specify the data accessors.
                .y(function (d) {
                    return d.value
                })
                .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
                .showValues(true);       //...instead, show the bar value right on top of each bar.

            chart.tooltip.enabled(false); //Don't show tooltips

            d3.select(selector)
                .datum([
                        {
                            values: data
                        }
                    ]
                )
                .call(chart)
                .append("a")
                .attr("href",function(d){return d.render_link;});

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }

    function render_pie(data,selector) {

        data = _.sortBy(data,function(d) {return d.value;}).slice(0,10)

        nv.addGraph(function () {
            var chart = nv.models.pieChart()
                .x(function (d) {
                    return d.label
                })
                .y(function (d) {
                    return d.value
                })
                .showLabels(true);

            chart.tooltip.enabled(false);

            d3.select(selector)
                .datum(data)
                .transition().duration(350)
                .call(chart);

            return chart;
        });
    }

    function render_treemap(data,selector) {

        var root = {
            label:"facet",
            children:data
        };

        function position() {
          this.style("left", function(d) { return d.x + "px"; })
              .style("top", function(d) { return d.y + "px"; })
              .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
              .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; })
              .style("font-size","15px").style("color","black");
}
        var margin = {top: 40, right: 10, bottom: 10, left: 10},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var color = d3.scale.category20c();
        var logs = d3.scale.sqrt();

        var treemap = d3.layout.treemap()
            .size([width, height])
            .sticky(true)
            .value(function(d) { return (logs(d.value)); });

        var div = d3.select(selector)
            .style("position", "relative")
            .style("width", (width + margin.left + margin.right) + "px")
            .style("height", (height + margin.top + margin.bottom) + "px")
            .style("left", margin.left + "px")
            .style("top", margin.top + "px");

      var node = div.datum(root).selectAll(".node")
          .data(treemap.nodes)
          .enter().append("div")
          .attr("class", "node")
          .call(position)
          .style("background", function(d) { return color(d.label); })
          .append("a").attr("href",function(d){return d.render_link;})
          .style("color","black")
          // .style("padding-top","15px")
          .text(function(d) { return  d.label; });


    }

    function render_creationdate(data,selector) {
        var year_sorted = _.sortBy(data,function(d) {return d.label;});
        console.log(year_sorted)

        if (year_sorted[0].label == 1) {
            year_sorted = year_sorted.slice(1,year_sorted.length);
        }

        var _max = year_sorted[year_sorted.length -1].label,
            _min = year_sorted[0].label;

        console.log(_min,_max);

        var diff = _max - _min;

        var interval = 1000;
        while (diff < interval) {
            interval /= 10;
        }

        console.log(diff,interval);

        var aggs = aggregate_data(year_sorted,interval);

        render_bar_d3(aggs,selector)
    }

    function aggregate_data(sorted,interval) {

        function _prfx(lnk) {
            return /\/render_facet\/\d+\/\?/.exec(lnk)[0];
        }

        function _intrvl(year) {
            return Math.floor(year/interval)*interval;
        }

        function _agg(d) {
            var agg = {};
            agg.label = _intrvl(d.label);
            agg.value = d.value;
            agg.render_link = _prfx(d.render_link) + "years=" + agg.label + "," + (agg.label+interval-1);
            console.log(agg);

            return agg;
        }

        var aggs = [];
        var agg = {};
        for (var i = 0;i < sorted.length;i++) {
            var d = sorted[i];
            if (agg.label === undefined) {
                agg = _agg(d);
                continue;
            }

            if (_intrvl(d.label) < (agg.label + interval)) {
                agg.value += d.value;
            } else {
                aggs.push(agg);
                agg = _agg(d)
            }
        }
        aggs.push(agg);

        if (aggs.length <= 2 && interval > 1) {
            return aggregate_data(sorted,interval/10);
        } else {
            return aggs;
        }

    }

    function render_bar_d3(data,selector) {

        var margin = {top: 20, right: 20, bottom: 40, left: 40},
            width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(10);

        var svg = d3.select(selector).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        x.domain(data.map(function(d) { return d.label; }));
        y.domain([0, d3.max(data, function(d) { return d.value; })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(90)")
            .style("text-anchor", "start");

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Count");

        svg.selectAll(".bar")
            .data(data)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.label); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); })
            .on("click",function(d) { window.location= d.render_link;});
    }

    return vis;
})();
