var rectMap_dimensions = {
    rectWidth: grid_width,
    rectHeight: grid_height,
    Width: width_gridmap,
    Height: height_gridmap
};

var tooltip = d3
    .select("#gridmap")
    .append("div")
    .attr("class", "toolTip");

var rectMap_color = d3
    .scaleLinear()
    .domain([0, 3.75, 7.5, 11.25, 15])
    .range(rangeRed);

var rectMap_svg = d3.select("svg"),
    rectMap_margin = margin,
    rectMap_width = +rectMap_svg.attr("width") - rectMap_margin.left - rectMap_margin.right,
    rectMap_height = +rectMap_svg.attr("height") - rectMap_margin.top - rectMap_margin.bottom;

var sEnter = rectMap_svg
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
            d.x * rectMap_dimensions.rectWidth +
            "," +
            d.y * rectMap_dimensions.rectHeight +
            ")"
        );
    });

sEnter
    .append("rect")
    .attr("width", rectMap_dimensions.rectWidth / 1.00)
    .attr("height", rectMap_dimensions.rectHeight / 1.00)
    .style("opacity", 1)
    .style("fill", function (d) {
        return rectMap_color(d.sus);
    })
    .style("stroke", "#1e1e1e")

    .on("mousemove", function (d) {
        var w = window.innerWidth;
        var h = window.innerHeight;
        tooltip
            .style("display", "inline-block")
            .html("Test" + "<br>" + "£" + "test");
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

sEnter
    .append("text")
    .attr("x", rectMap_dimensions.rectWidth / 2)
    .attr("y", rectMap_dimensions.rectHeight / 1.75)
    .style("text-anchor", "middle")
    .style("pointer-events", "none")
    .text(function (d) {
        return d.key;
    });

var legend = rectMap_svg
    .selectAll(".legend")
    .data(rectMap_color.domain())
    .enter()
    .append("g")
    .attr("class", "legend")
    .attr("transform", function (d, i) {
        return "translate(" + i * 80 + ",0)";
    });

legend
    .append("rect")
    .attr("x", rectMap_dimensions.Width / 4)
    .attr("y", 700)
    .attr("width", 80)
    .attr("height", 20)
    .style("fill", rectMap_color);

legend.append("text")
    .attr("x", rectMap_dimensions.Width / 4)
    .attr("y", 740)
    .attr("dy", ".45em")
    .style("text-anchor", "start")
    .attr("transform", function (d, i) {
        return "translate(" + i * 13 + ",0)";
    })
    .text(function (d) {
        return d + '%';
    });

var legendtri = rectMap_svg
    .append("svg")
    .attr("width", rectMap_dimensions.Width)
    .attr("height", rectMap_dimensions.Height);

legendtri
    .append("path") // attach a path
    .style("stroke", "none") // colour the line
    .style("fill", "#1e1e1e") // remove any fill colour
    .attr("d", "M 0,0, L 30,0, L 15,20 Z")
    .attr("transform", function (d, i) {
        return "translate(" + (rectMap_dimensions.Width / 2 - 15) + "," + 690 + ")";
    });

legendtri
    .append("text")
    .attr("x", 0)
    .attr("y", rectMap_dimensions.Height - 130)
    .attr("transform", function (d, i) {
        return "translate(" + rectMap_dimensions.Width / 2 + "," + 0 + ")";
    })
    .attr("dy", ".45em")
    .style("text-anchor", "middle")
    .style("fill", "white")
    .text("national average");