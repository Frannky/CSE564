function drawLinePlot(data, div, groups, myX, myWidth, myHeight, myMargin) {
    // var tooltip = d3
    // .select(div)
    // .append("div")
    // .attr("class", "toolTip");

    var width = myWidth - myMargin.left - myMargin.right,
        height = myHeight - myMargin.top - myMargin.bottom;

    var dataReady = groups.map(function (group) { // .map allows to do something for each element of the list
        return {
            group: group,
            groupValues: data.filter(function (d) {
                return d.group == groups.indexOf(group);
            })
        };
    });

    var myColor = d3.scaleOrdinal()
        .domain(d3.extent(dataReady, function (d) {
            return d.group;
        }))
        .range(myColorSet);

    var x = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d.x;
        }))
        .range([myMargin.left, myWidth - myMargin.right]);

    var y = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d.y;
        }))
        .range([myHeight - myMargin.bottom, myMargin.top])
    ;

    var svg = d3.select(div).select("svg");
    svg
        .attr("width", myWidth)
        .attr("height", myHeight)
        .append("g")
        .attr("transform",
            "translate(" + (myMargin.left) + "," + myMargin.top + ")");

    var xAxis = d3.axisBottom(x)
        .tickValues(myX)
        .tickFormat(d3.format("d"));

    svg.append("g")
        .attr("transform", "translate(0," + (myHeight - myMargin.bottom) + ")")
        .call(xAxis)
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + "0)")
        .call(d3.axisLeft(y))
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    var myLine = d3.line()
        .x(function (d) {
            return x(+d.x)
        })
        .y(function (d) {
            return y(+d.y)
        })

    svg.selectAll("myLines")
        .data(dataReady)
        .enter()
        .append("path")
        .attr("class", function (d) {
            return "myclass"+groups.indexOf(d.group)
        })
        .attr("d", function (d) {
            return myLine(d.groupValues)
        })
        .style("stroke", function (d) {
            return myColor(d.group)
        })
        .style("stroke-width", 4)
        .style("fill", "none")

    svg
        .selectAll("myDots")
        .data(dataReady)
        .enter()
        .append('g')
        .style("fill", function (d) {
            return myColor(d.group)
        })
        .attr("class", function (d) {
            return "myclass"+groups.indexOf(d.group)
        })
        .selectAll("myPoints")
        .data(function (d) {
            return d.groupValues
        })
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return x(d.x)
        })
        .attr("cy", function (d) {
            return y(d.y)
        })
        .attr("r", 5)
        .attr("stroke", "white")

    // svg
    //     .selectAll("myLabels")
    //     .data(dataReady)
    //     .enter()
    //     .append('g')
    //     .append("text")
    //     .attr("class", function (d) {
    //         return "myclass"+groups.indexOf(d.group)
    //     })
    //     .datum(function (d) {
    //         return {group: d.group, groupValues: d.groupValues[d.groupValues.length - 1]};
    //     })
    //     .attr("transform", function (d) {
    //         return "translate(" + x(d.groupValues.x) + "," + y(d.groupValues.y) + ")";
    //     })
    //     .attr("x", 12)
    //     .text(function (d) {
    //         return d.group;
    //     })
    //     .style("fill", function (d) {
    //         return myColor(d.group)
    //     })
    //     .style("font-size", 15)

    svg
        .selectAll("myLegend")
        .data(dataReady)
        .enter()
        .append('g')
        .append("text")
        .attr('x', function (d, i) {
            return 30 + (i % 3) * 200
        })
        .attr('y', function (d, i) {
            return 30 + Math.floor((i / 3)) * 30
        })
        .text(function (d) {
            return d.group;
        })
        .style("fill", function (d) {
            return myColor(d.group)
        })
        .style("font-size", 15)
        .on("click", function (d) {
            currentOpacity = d3.selectAll("." + "myclass" + groups.indexOf(d.group)).style("opacity");
            d3.selectAll("." + "myclass" + groups.indexOf(d.group)).transition().style("opacity", currentOpacity == 1 ? 0 : 1)

        })
}

function drawLinePlotDash(data, div, groups, myX, myWidth, myHeight, myMargin) {
    // var tooltip = d3
    // .select(div)
    // .append("div")
    // .attr("class", "toolTip");

    var width = myWidth - myMargin.left - myMargin.right,
        height = myHeight - myMargin.top - myMargin.bottom;

    var dataReady = groups.map(function (group) { // .map allows to do something for each element of the list
        return {
            group: group,
            groupValues: data.filter(function (d) {
                return d.group == groups.indexOf(group);
            })
        };
    });

    var myColor = d3.scaleOrdinal()
        .domain(d3.extent(dataReady, function (d) {
            return d.group;
        }))
        .range(myColorSet);

    var x = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d.x;
        }))
        .range([myMargin.left, myWidth - myMargin.right]);

    var y = d3.scaleLinear()
        .domain(d3.extent(data, function (d) {
            return d.y;
        }))
        .range([myHeight - myMargin.bottom, myMargin.top])
    ;

    var svg = d3.select(div).select("svg");
    svg
        .attr("width", myWidth)
        .attr("height", myHeight)
        .append("g")
        .attr("transform",
            "translate(" + (myMargin.left) + "," + myMargin.top + ")");

    var xAxis = d3.axisBottom(x)
        .tickValues(myX)
        .tickFormat(d3.format("d"));

    svg.append("g")
        .attr("transform", "translate(0," + (myHeight - myMargin.bottom) + ")")
        .call(xAxis)
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + "0)")
        .call(d3.axisLeft(y))
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    var myLine = d3.line()
        .x(function (d) {
            return x(+d.x)
        })
        .y(function (d) {
            return y(+d.y)
        })

    svg.selectAll("myLines")
        .data(dataReady)
        .enter()
        .append("path")
        .attr("class", function (d) {
            return "myclass"+groups.indexOf(d.group)
        })
        .attr("d", function (d) {
            return myLine(d.groupValues)
        })
        .style("stroke", function (d) {
            return myColor(d.group)
        })
        .style("stroke-width", 4)
        .style("fill", "none")

    svg
        .selectAll("myDots")
        .data(dataReady)
        .enter()
        .append('g')
        .style("fill", function (d) {
            return myColor(d.group)
        })
        .attr("class", function (d) {
            return "myclass"+groups.indexOf(d.group)
        })
        .selectAll("myPoints")
        .data(function (d) {
            return d.groupValues
        })
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return x(d.x)
        })
        .attr("cy", function (d) {
            return y(d.y)
        })
        .attr("r", 5)
        .attr("stroke", "white")

    // svg
    //     .selectAll("myLabels")
    //     .data(dataReady)
    //     .enter()
    //     .append('g')
    //     .append("text")
    //     .attr("class", function (d) {
    //         return "myclass"+groups.indexOf(d.group)
    //     })
    //     .datum(function (d) {
    //         return {group: d.group, groupValues: d.groupValues[d.groupValues.length - 1]};
    //     })
    //     .attr("transform", function (d) {
    //         return "translate(" + x(d.groupValues.x) + "," + y(d.groupValues.y) + ")";
    //     })
    //     .attr("x", 12)
    //     .text(function (d) {
    //         return d.group;
    //     })
    //     .style("fill", function (d) {
    //         return myColor(d.group)
    //     })
    //     .style("font-size", 15)

    svg
        .selectAll("myLegend")
        .data(dataReady)
        .enter()
        .append('g')
        .append("text")
        .attr('x', function (d, i) {
            return 30 + (i % 3) * 200
        })
        .attr('y', function (d, i) {
            return 30 + Math.floor((i / 3)) * 30
        })
        .text(function (d) {
            return d.group;
        })
        .style("fill", function (d) {
            return myColor(d.group)
        })
        .style("font-size", 15)
        .on("click", function (d) {
            currentOpacity = d3.selectAll("." + "myclass" + groups.indexOf(d.group)).style("opacity");
            d3.selectAll("." + "myclass" + groups.indexOf(d.group)).transition().style("opacity", currentOpacity == 1 ? 0 : 1)

        })
}