var width = width_heatmap - margin.left - margin.right,
    height = height_heatmap - margin.top - margin.bottom;

function drawHeatmap(data, div) {
    // var xAxisName = data.shift().group;
    // var yAxisName = xAxisName;

    var tooltip = d3
    .select(div)
    .append("div")
    .attr("class", "toolTip");

    var xAxisName = ['STATUS', 'STATE', 'TOTAL', 'WAGE', 'PW', 'YEAR', 'OCCUPATION']
    var yAxisName = xAxisName;

    var x = d3.scaleBand()
        .range([0, width])
        .domain(xAxisName)
        .padding(padding_heatmap);
    var y = d3.scaleBand()
        .range([height, 0])
        .domain(yAxisName)
        .padding(padding_heatmap);

    var svg = d3.select("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
    svg.append("g")
        .call(d3.axisLeft(y));

    var color = d3.scaleLinear()
    .range(rangeRed)
    .domain([-1, 1])

    drawDataHeatmap(data, svg, x, y, color)
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
        })
}