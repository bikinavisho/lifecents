/**
 * Created by bianca on 4/6/17.
 */
// income_data
// expense_data

var pie_dimension = $(".shell").css("width");
pie_dimension *= (1/3);


$(document).ready(function() {
    //PIE CHART CODE	=================================================
(function(d3) {window.alert("Triggered");
    //Step 1: Define some data

    var dataset = [
		{ label: 'Apple', count: 80 },
		{ label: 'Banana', count: 20 },
		{ label: 'Orange', count: 30 },
		{ label: 'Grape', count: 99 }
	];
	//These  entries correspond to the four segments in our chart

	//Step 2: Define Dimensions for chart
	var width = 200;
	var height = 200;
	var radius = Math.min(width, height) / 2;

	//Define a color scale for chart
	//var color = d3.scale.category20c();
	//Alternatively, could have done the following with our own color palette
	var color = d3.scale.ordinal()
	 		.range(['#cedb9c', '#b5cf6b', '#8ca252', '#637939']);

	//Now, create svg!
	var svg = d3.select('#chart1')		//select method to retreive DOM element with id chart
		.append('svg')					// append svg element to ^ selected element
		.attr('width', width)			// set width of svg
		.attr('height', height)			// set height of svg
		.append('g')					// append g element to svg element
		.attr('transform', 'translate(' + (width/2) + ',' + (height/2) + ')');
										// center g element within containing svg element

	var donutWidth = 75;

	//Step 4: Define the radius
	var arc = d3.svg.arc()
		.innerRadius(radius - donutWidth)		//This makes it a donut! W/out this, is a pie.
		.outerRadius(radius);
	//Step 5: Define the start and end angles of the segments
	var pie = d3.layout.pie()
		.value(function(d) {	return d.count;	})
		.sort(null);		//disables sorting of entries b/c already in order
							//also sorting will mess with animation later
		// Count helps to define how to extract numerical data from each entry in our dataset

	//Step 6: Create Pie Chart!!
	var path = svg.selectAll('path')		//select all path elements inside our svg(g)
		.data(pie(dataset))					//associate our dataset with the path elements to create															//pie function knows how to extract the values and
											//  give them meaning in the context of a pie chart
		.enter()							//creates placeholder nodes for each of the values in dataset
		.append('path')						//replace our placeholders with path elements
		.attr('d', arc)						//define d attribute using arc function
		.attr('fill', function(d, i) {		//use color scale to fill each path by associating color with label
			return color(d.data.label);
		});


    var arc3 = d3.svg.arc()
        .outerRadius(radius)
        .innerRadius(0);

    // Add the labels
    var arcs = svg.selectAll("g.slice")
        .data(pie(dataset))
        .enter()
            .append("g")
                .attr("class", "slice");
        arcs.append("text")
        .attr("transform", function(d) {
            d.innerRadius = 0;
            d.outerRadius = radius;
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("text-anchor", "middle")
        .attr("font-size", "1em")
        .attr("class", "pie-label")
        .text(function(d, i) {	return dataset[i].label});

      //Sets labels to hidden by default
        arcs.classed("hidden", true);

    path.on('mouseover', function(d) {
        arcs.classed("hidden", false);
    });
    path.on('mouseout', function(d) {
        arcs.classed("hidden", true);
    });

    })(window.d3);


	
});

