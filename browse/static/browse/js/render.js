/**
 * Created by azk on 15/12/15.
 */

"use strict";

(function () {

    var vis = {
        choose_facet: function(facet_data) {
                return decide(facet_data);
                //return "creationdate";
            },

        render_facet: function(name,data,selector) {
            if (name == "creationdate") {
                render_creationdate(data, selector)
            } else {
                render_other(data, selector)
            }
        }};

        function decide(facet_data) {
                var num_facets = Object.keys(facet_data).length;
                var idx = Math.floor(Math.random()*num_facets);

                console.log("Idx: ",idx);
                return Object.keys(facet_data)[idx];
        }

        function render_creationdate(data,selector) {

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

        function render_other(data,selector) {

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

    this.facetVis = vis
}).call(this);
