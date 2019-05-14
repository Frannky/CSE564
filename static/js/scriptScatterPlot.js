var width = width_scatterPlot - margin.left - margin.right,
    height = height_scatterplot - margin.top - margin.bottom;

var x = d3.scale.linear()
    .range([0, width]);
var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);
var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

// Define the line
var valueline = d3.svg.line()
//.x(function(d) { return x(d.date); })
    .x(function (d) {
        return x(d.x);
    })
    //.y(function(d) { return y(d.close); });
    .y(function (d) {
        return y(d.y);
    });

function drawLinePlot(data, div) {
    // Scale the range of the data
    x.domain(d3.extent(data, function (d) {
        return d.x;
    }));
    y.domain([0, d3.max(data, function (d) {
        return d.y;
    })]);

    // Adds the svg canvas for raw data
    var svg = d3.select(div)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
        // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));
}

function drawScatterPlot(data, div) {
    x.domain(d3.extent(data, function (d) {
        return d.x;
    }));
    y.domain(d3.extent(data, function (d) {
        return d.y;
    }));

    var svg = d3.select(div)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    svg.append("g")
        .selectAll("dot")
        .data(data).enter()
        .append("circle")
        .attr("cx", function (d) {
            return x(d.x)
        })
        .attr("cy", function (d) {
            return y(d.y)
        })
        .attr("r", 1)
        .style("fill", "#168eb9");
}