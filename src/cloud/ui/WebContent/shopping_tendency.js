var data = {
    pieChart  : []
};

var DURATION = 1000;
var DELAY    = 500;

/**
 * draw the fancy pie chart
 *
 * @param {String} elementId elementId
 * @param {Array}  data      data
 */
function drawPieChart( elementId, data ) {
    // TODO code duplication check how you can avoid that
    var containerEl = document.getElementById( elementId ),
        width       = containerEl.clientWidth,
        height      = width * 0.6,
        radius      = Math.min( width, height, width * 0.4 ) / 2,
        container   = d3.select( containerEl ),
        svg         = container.select( 'svg' )
            .attr( 'width', width )
            .attr( 'height', height );
    var pie = svg.append( 'g' )
        .attr(
            'transform',
            'translate(' + width / 2 + ',' + height / 2 + ')'
        );

    var detailedInfo = svg.append( 'g' )
        .attr( 'class', 'pieChart--detailedInformation' );

    var twoPi   = 2 * Math.PI;
    var pieData = d3.layout.pie()
        .value( function( d ) { return d.value; } );

    var arc = d3.svg.arc()
        .outerRadius( radius - 20)
        .innerRadius( 0 );

    var pieChartPieces = pie.datum( data )
        .selectAll( 'path' )
        .data( pieData )
        .enter()
        .append( 'path' )
        .attr( 'class', function( d ) {
            return 'pieChart__' + d.data.color;
        } )
        .attr( 'filter', 'url(#pieChartInsetShadow)' )
        .attr( 'd', arc )
        .each( function() {
            this._current = { startAngle: 0, endAngle: 0 };
        } )
        .transition()
        .duration( DURATION )
        .attrTween( 'd', function( d ) {
            var interpolate = d3.interpolate( this._current, d );
            this._current = interpolate( 0 );

            return function( t ) {
                return arc( interpolate( t ) );
            };
        } )
        .each( 'end', function handleAnimationEnd( d ) {
            drawDetailedInformation( d.data, this );
        } );

    drawChartCenter();

    function drawChartCenter() {
        var centerContainer = pie.append( 'g' )
            .attr( 'class', 'pieChart--center' );

        centerContainer.append( 'circle' )
            .attr( 'class', 'pieChart--center--outerCircle' )
            .attr( 'r', 0 )
            .attr( 'filter', 'url(#pieChartDropShadow)' )
            .transition()
            .duration( DURATION )
            .delay( DELAY )
            .attr( 'r', radius - 50 );

        centerContainer.append( 'circle' )
            .attr( 'id', 'pieChart-clippy' )
            .attr( 'class', 'pieChart--center--innerCircle' )
            .attr( 'r', 0 )
            .transition()
            .delay( DELAY )
            .duration( DURATION )
            .attr( 'r', radius - 55 )
            .attr( 'fill', '#fff' );
    }

    function drawDetailedInformation ( data, element ) {
        var bBox      = element.getBBox(),
            infoWidth = width * 0.3,
            anchor,
            infoContainer,
            position;

        if ( ( bBox.x + bBox.width / 2 ) > 0 ) {
            infoContainer = detailedInfo.append( 'g' )
                .attr( 'width', infoWidth )
                .attr(
                    'transform',
                    'translate(' + ( width - infoWidth ) + ',' + ( bBox.height + bBox.y + 80 ) + ')'
                );
            anchor   = 'end';
            position = 'right';
        } else {
            infoContainer = detailedInfo.append( 'g' )
                .attr( 'width', infoWidth )
                .attr(
                    'transform',
                    'translate(' + 0 + ',' + ( bBox.height + bBox.y + 80 ) + ')'
                );
            anchor   = 'start';
            position = 'left';
        }

        infoContainer.data( [ data.value * 100 ] )
            .append( 'text' )
            .text ( '0 %' )
            .attr( 'class', 'pieChart--detail--percentage' )
            .attr( 'x', ( position === 'left' ? 0 : infoWidth ) )
            .attr( 'y', -10 )
            .attr( 'text-anchor', anchor )
            .transition()
            .duration( DURATION )
            .tween( 'text', function( d ) {
                var i = d3.interpolateRound(
                    +this.textContent.replace( /\s%/ig, '' ),
                    d
                );

                return function( t ) {
                    this.textContent = i( t ) + ' %';
                };
            } );

        infoContainer.append( 'line' )
            .attr( 'class', 'pieChart--detail--divider' )
            .attr( 'x1', 0 )
            .attr( 'x2', 0 )
            .attr( 'y1', 0 )
            .attr( 'y2', 0 )
            .transition()
            .duration( DURATION )
            .attr( 'x2', infoWidth );

        infoContainer.data( [ data.description ] )
            .append( 'foreignObject' )
            .attr( 'width', infoWidth )
            .attr( 'height', 100 )
            .append( 'xhtml:body' )
            .attr(
                'class',
                'pieChart--detail--textContainer ' + 'pieChart--detail__' + position
            )
            .html( data.description );
    }
}

function handleResult(resultData) {
    console.log(resultData);
    let color = ['red', 'blue'];
    let curColor = 0;
    for(let i = 0; i < resultData.length; i++)
    {
        data.pieChart.push({
            color: color[curColor],
            description: resultData[i].item,
            title: resultData[i].item,
            value: resultData[i].percentage
        });
        if (curColor == 0){
            curColor = 1;
        }
        else{
            curColor = 0;
        }
    }
    console.log(data.pieChart);
    drawPieChart( 'pieChart', data.pieChart );
}


// ##################################
jQuery.ajax({
    dataType: "json",
    method: "GET",
    url: "api/shopping-tendency",
    success: (resultData) => handleResult(resultData)
});