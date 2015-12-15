/**
 * Created by azk on 15/12/15.
 */

"use strict";

function choose_facet(facet_data) {
    return decide(facet_data);
    //return "creationdate";
}

function decide(facet_data) {
    var num_facets = Object.keys(facet_data).length;
    var idx = Math.floor(Math.random()*num_facets)

    console.log("Idx: ",idx);
    return Object.keys(facet_data)[idx];
}

function render_facet(name,data,selector) {
    if (name == "creationdate") {
        render_creationdate(data,selector)
    } else {
        render_other(data,selector)
    }

}


function render_creationdate(data,selector) {
    nv.addGraph(function() {
      var chart = nv.models.discreteBarChart()
          .x(function(d) { return d.label })    //Specify the data accessors.
          .y(function(d) { return d.value })
          .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
          .tooltips(false)        //Don't show tooltips
          .showValues(true);       //...instead, show the bar value right on top of each bar.


      d3.select(selector)
          .datum([
              {
                  values    :   data
              }
          ]
          )
          .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
}

function render_other(data,selector) {
        nv.addGraph(function() {
          var chart = nv.models.pieChart()
              .x(function(d) { return d.label })
              .y(function(d) { return d.value })
              .showLabels(true);

            d3.select(selector)
                .datum(data)
                .transition().duration(350)
                .call(chart);

          return chart;
        });
}