function drawGridMap(data, dataname, categoryname, states, domain, div, divSvg, myWidth, myHeight, myGridWidth, myGridHeight, myMargin, withLegend) {
    var tooltip = d3
        .select(div)
        .append("div")
        .attr("class", "toolTip");

    var color = d3
        .scaleLinear()
        .domain(domain)
        .range(rangeGreen);

    var svgMap = d3.select(divSvg);

    var width = svgMap.attr("Width") - myMargin.left - myMargin.right,
        height = svgMap.attr("Height") - myMargin.top - myMargin.bottom;

    var xLegend = myWidth / 4,
        yLegend = 700,
        widthLegend = 80,
        heightLegend = 20;

    if (withLegend) {
        var legend = svgMap
            .selectAll(".legend")
            .data(color.domain())
            .enter()
            .append("g")
            .attr("class", "legend")
            .attr("transform", function (d, i) {
                return "translate(" + i * 80 + ",0)";
            });

        legend
            .append("rect")
            .attr("x", xLegend)
            .attr("y", yLegend)
            .attr("width", widthLegend)
            .attr("height", heightLegend)
            .style("fill", color);

        legend
            .append("text")
            .attr("x", xLegend)
            .attr("y", yLegend + 40)
            .attr("dy", ".45em")
            .style("text-anchor", "start")
            .attr("transform", function (d, i) {
                return "translate(" + i * 13 + ",0)";
            })
            .text(function (d) {
                return d;
            })
            .style("fill", "#BBB");

        var legendtri = svgMap
            .append("svg")
            .attr("width", myWidth)
            .attr("height", myHeight);

        legendtri
            .append("path")
            .style("stroke", "none")
            .style("fill", "#1e1e1e")
            .attr("d", "M 0,0, L 30,0, L 15,20 Z")
            .attr("transform", function (d, i) {
                return "translate(" + (myWidth / 2 - 15) + "," + 690 + ")";
            });

        legendtri
            .append("text")
            .attr("x", 0)
            .attr("y", myHeight - 130)
            .attr("transform", function (d, i) {
                return "translate(" + myWidth / 2 + "," + 0 + ")";
            })
            .attr("dy", ".45em")
            .style("text-anchor", "middle")
            .style("fill", "#BBB")
            .text(function () {
                return categoryname == "none" ? dataname : dataname + " in " + categoryname;
            });
    }
    drawDataGridmap(data, dataname, states, svgMap, myGridWidth, myGridHeight, color, tooltip);
}

// function updateDataGridmap(data, dataname, categoryName, states, domain, myGridWidth, myGridHeight) {
//     var color = d3
//     .scaleLinear()
//     .domain(domain)
//     .range(rangeGreen);
//
//     d3.selectAll(".legend")
//         .data(color.domain())
//         .enter();
//      var tooltip = d3.selectAll(".tooltip")
//     .text(function (d) {
//             return d;
//         })
//     legendtri
//         .text(function () {
//             return categoryname == "none" ? dataname : dataname + " in " + categoryname;
//         });
//
//     for (var i = 0; i < states.length; i++) {
//         svgRect = d3.selectAll(".myRec" + i)
//             .style("fill", function (d) {
//                 return color(data[i]);
//             })
//             .on("mousemove", function (d) {
//                 var w = window.innerWidth;
//                 var h = window.innerHeight;
//                 tooltip
//                     .style("display", "inline-block");
//                 if (data[states.indexOf(d.key)] == null) {
//                     tooltip
//                         .html("Data Missing");
//                 }
//                 else {
//                     tooltip
//                         .html(dataname + ": " + "<br>" + data[states.indexOf(d.key)]);
//                 }
//             })
//     }
// }

function drawDataGridmap(data, dataname, states, svg, myGridWidth, myGridHeight, color, tooltip) {
    var svgRect = d3.select("svg")
        .append("g")
        .selectAll("g")
        .data(gridmapLayoutUsa)
        .enter()
        .append("g")
        .attr("id", function (d) {
            return d.key;
        })
        .attr("transform", function (d) {
            return (
                "translate(" +
                d.x * myGridWidth +
                "," +
                d.y * myGridHeight +
                ")"
            );
        });

    svgRect
        .append("rect")
        .attr("class", function (d) {
            return "myRec" + states.indexOf(d.key);
        })
        .attr("width", myGridWidth / 1.00)
        .attr("height", myGridHeight / 1.00)
        .style("opacity", function(d){
            return data[states.indexOf(d.key)] == null ? 0 : 1;
        })
        .style("fill", function (d) {
            return color(data[states.indexOf(d.key)]);
        })
        .style("stroke", "#1e1e1e")
        .on("mousemove", function (d) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            tooltip
                .style("display", "inline-block");
            if (data[states.indexOf(d.key)] == null) {
                // tooltip
                //     .html("Data Missing");
                tooltip.style("display", "none");
            }
            else {
                tooltip
                    .html(dataname + ": " + "<br>" + data[states.indexOf(d.key)]);
            }
            tooltip.style("left", d3.event.pageX - 80 - 200 + "px");
            if (d3.event.pageY < h / 3) {
                tooltip.style("top", d3.event.pageY + 20 + "px");
            } else {
                tooltip.style("top", d3.event.pageY - 70 + "px");
            }
        })
        .on("mouseout", function (d) {
            tooltip.style("display", "none");
        })
        .on("click", function (d) {
            if (data[states.indexOf(d.key)] != null) {
                currentOpacity = d3.select(this).style("opacity");
                d3.select(this).transition().style("opacity", currentOpacity == 1 ? 0.3 : 1)
            }

        })
    ;

    svgRect
        .append("text")
        .attr("x", myGridWidth / 2)
        .attr("y", myGridHeight / 1.75)
        .style("text-anchor", "middle")
        .style("pointer-events", "none")
        .text(function (d) {
            return d.key;
        });
}

