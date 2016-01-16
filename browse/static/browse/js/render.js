/**
 * Created by azk on 15/12/15.
 */

"use strict";

var facetVis = (function () {

    var vis = {
        render_facet: function(name,data,selector) {
                if (name == "creationdate") {
                    render_bar(data, selector)
                } else {
                    render_pie(data, selector)
                }
        },
        render_facets: function(all_facets,num_render,selector,ranks) {
            ranks = (typeof ranks === 'undefined') ? this.rank_facets(all_facets):ranks;

            if (ranks.length < num_render) {
                num_render = ranks.length
            }

            for (var i = 0;i < num_render; i++) {
                var _id = "facet" + i
                var svg = $("<svg id='" + _id + "' style='height:500px'></svg>" )
                $(selector).append(svg)
                this.render_facet(ranks[i],all_facets[ranks[i]],"#" + _id)
            }
        },
        rank_facets: function(all_facets,total_hits) {

            var ranks  =  _.intersection( _.keys(facet_pretty_names),_.keys(all_facets));
            console.log(ranks);
            return ranks
        }

    };

    function render_bar(data,selector) {

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
                .call(chart);

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

    return vis;
})();
