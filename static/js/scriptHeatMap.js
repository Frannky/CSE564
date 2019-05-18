// TODO: range of color should be changed
function drawHeatmap(data, groupData, div, myWidth, myHeight, myMargin) {
    var width = myWidth - myMargin.left - myMargin.right,
    height = myHeight - myMargin.top - myMargin.bottom;
    var xAxisName = groupData;
    var yAxisName = xAxisName;

    var x = d3.scaleBand()
        .range([0, width - margin.left - margin.right])
        .domain(xAxisName)
        .padding(padding_heatmap);
    var y = d3.scaleBand()
        .range([height - margin.top - margin.bottom, 0])
        .domain(yAxisName)
        .padding(padding_heatmap);

    var svg = d3.select("svg")
        .attr("width", width+50)
        .attr("height", height)
        .append("g")
        .attr("transform",
            "translate(" + (margin.left + 50) + "," + margin.top + ")");

    var xAxis = svg.append("g")
        .attr("transform", "translate(0," + (height - margin.bottom - margin.top) + ")")
        .call(d3.axisBottom(x))
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    var yAxis = svg.append("g")
        .call(d3.axisLeft(y))
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    var color = d3.scaleLinear()
    .range(rangeRed)
    .domain([-1, 1]);

    drawDataHeatmap(data, svg, x, y, color);
}

function drawDataHeatmap(data, svg, x, y, color) {
    svg.selectAll()
        .data(data, function (d) {
            return d.x + ':' + d.y;
        })
        .enter()
        .append("rect")
        .attr("x", function (d) {
            return x(d.x)
        })
        .attr("y", function (d) {
            return y(d.y)
        })
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function (d) {
            return color(d.value)
        });
}