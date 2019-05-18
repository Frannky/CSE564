function drawGridMap(data, dataname, states, domain, div, myWidth, myHeight, myGridWidth, myGridHeight, myMargin) {
    var tooltip = d3
        .select(div)
        .append("div")
        .attr("class", "toolTip");

    var svgMap = d3.select("svg");

    var width = svgMap.attr("Width") - myMargin.left - myMargin.right,
        height = svgMap.attr("Height") - myMargin.top - myMargin.bottom;

    var xLegend = myWidth / 4,
        yLegend = 700,
        widthLegend = 80,
        heightLegend = 20;

    var color = d3
    .scaleLinear()
    .domain(domain)
    .range(rangeRed);

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
        .text(dataname);

    drawDataGridmap(data, dataname, states, svgMap, myGridWidth, myGridHeight, color, tooltip);
}

function drawDataGridmap(data, dataname, states, svg, myGridWidth, myGridHeight, color, tooltip) {
    var svgRect = svg
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
        .attr("width", myGridWidth / 1.00)
        .attr("height", myGridHeight / 1.00)
        .style("opacity", 1)
        .style("fill", function (d) {
            return color(data[states.indexOf(d.key)]);
        })
        .style("stroke", "#1e1e1e")
        .on("mousemove", function (d) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            tooltip
                .style("display", "inline-block");
            if (data[states.indexOf(d.key)] == null)
            {
                tooltip
                    .html("Data Missing");
            }
            else {
                tooltip
                    .html(dataname + ": " + "<br>" + data[states.indexOf(d.key)]);
            }
            if (d3.event.pageX < w / 2) {
                tooltip.style("left", d3.event.pageX + 20 + "px");
            } else {
                tooltip.style("left", d3.event.pageX - 80 + "px");
            }
            if (d3.event.pageY < h / 3) {
                tooltip.style("top", d3.event.pageY + 20 + "px");
            } else {
                tooltip.style("top", d3.event.pageY - 70 + "px");
            }
        })

        .on("mouseout", function (d) {
            tooltip.style("display", "none");
        });

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