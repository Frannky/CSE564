function drawStackedBarChart(data, div, myGroup, myX, myWidth, myHeight, myMargin) {

    var width = myWidth - myMargin.left - myMargin.right,
        height = myHeight - myMargin.top - myMargin.bottom;

    var dataReady = d3.stack().keys(myGroup)(data);

    var myColor = d3.scaleOrdinal()
        .domain(d3.extent(dataReady, function (d, i) {
            return i;
        }))
        .range(myColorSet);

    var x = d3.scaleBand()
        .domain(myX)
        .range([myMargin.left, myWidth - myMargin.right - 200]);

    var y = d3.scaleLinear();
    y.domain([0, d3.max(data, function(d) { return d.total; })]).nice();
    y.range([myHeight - myMargin.bottom, myMargin.top]);

    var xAxis = d3.axisBottom(x)
        .tickValues(myX)
        .tickFormat(d3.format("d"));

    var svg = d3.select("svg");
    svg
        .attr("width", myWidth)
        .attr("height", myHeight)
        .append("g")
        .attr("transform",
            "translate(" + (myMargin.left) + "," + myMargin.top + ")");

    svg.append("g")
        .attr("transform", "translate(0," + (myHeight - myMargin.bottom) + ")")
        .call(xAxis)
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    svg.append("g")
        .attr("transform", "translate(" + myMargin.left + "," + "0)")
        .call(d3.axisLeft(y))
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

    svgRect = svg
        .selectAll("myBars")
        .data(dataReady)
        .enter()
        .append('g')
        .style("fill", (d, i) => (myColor(i)))
        .attr("class", function (d, i) {
            return "myclass" + i
        })
        .selectAll("myRects")
        .data(d => d)
        .enter()

    var tooltip = d3
        .select(div)
        .append("div")
        .attr("class", "toolTip");

    svgRect
        .append("rect")
        .attr("x", (d, i) => x(d.data.x) + x.bandwidth() / 4)
        .attr('y', d => y(d[1]))
        .attr('width', x.bandwidth() / 2)
        .attr('height', d => y(d[0]) - y(d[1]))

    .on("mouseover", function() { tooltip.style("display", null); })
        .on("mouseout", function () {
            tooltip.style("display", "none");
        })
        .on("mousemove", function (d) {
      //       var xPosition = d3.mouse(this)[0] - 5;
      // var yPosition = d3.mouse(this)[1] - 5;
      // tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
      // tooltip.select("text").text(d[1]-d[0]);
            var w = window.innerWidth;
            var h = window.innerHeight;
            tooltip
                .style("display", "inline-block");
                tooltip
                    .html(d[1]-d[0]);
                tooltip.style("left", d3.event.pageX + 50 - 300 + "px");
                tooltip.style("top", d3.event.pageY - 10 + "px");
        });


    var legend = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
        .data(myGroup)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(0," + (25+i * 30) + ")";
        });

    legend.append("rect")
        .attr("x", width -200)
        .attr("width", 20)
        .attr("height", 20)
        .attr("fill", (d, i) => (myColor(i)));

    legend.append("text")
        .attr("x", width - 210)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(function (d, i) {
            return myGroup[i];
        })
        .style("stroke", "#BBB")
        .style("stroke-width", "1");

  //       var tooltip = svg.append("g")
  //   .attr("class", "tooltip")
  //   .style("display", "none");
  //
  // tooltip.append("rect")
  //   .attr("width", 60)
  //   .attr("height", 20)
  //   .attr("fill", "white")
  //   .style("opacity", 0.5);
  //
  // tooltip.append("text")
  //   .attr("x", 30)
  //   .attr("dy", "1.2em")
  //   .style("text-anchor", "middle")
  //   .attr("font-size", "12px")
  //   .attr("font-weight", "bold");
}