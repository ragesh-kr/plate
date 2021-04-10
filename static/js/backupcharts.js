<script type="text/javascript">
    
    $('#inputGroupSelect02').on('change', function() {
       alert('test');
    });
</script>
<script type="text/javascript">
    var bstPerfBar = document.getElementById('bstPerfBar');
    var bstPerfBar_chart = new Chart(bstPerfBar,{
    type : 'bar',
    data : {
        labels : {{xaxis_bstPerfBar|safe}},
        datasets : {{dataset_bstPerf|safe}}

    },
    options: {
        title: {
            display: true,
            text: 'Items generating more revenue'
        },
        legend: {
            display: false
        },
        scales: {
            xAxes: [{

                display : true,
                scaleLabel :{
                    display : true,
                    labelString : 'Items'
                }           
            }],
            yAxes: [{
                    scaleLabel :{
                    display : true,
                    labelString : 'Total Amount'
                } 

            }]
        }
    }

});
</script>
<script type="text/javascript">
var ctx = document.getElementById('myChart');

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{xaxis_categoryTrend|safe}},
        datasets: {{data_categoryTrend|safe}}
    },
    options: {
    	title: {
            display: true,
            text: 'Category wise Trend'
        },
        scales: {
        	xAxes: [{
                
                type : 'time',
                distribution: 'series',
                 time : {
                    displayFormats : {
                        day: 'MMM D'
                    }              

                },
        		display : true,
        		scaleLabel :{
        			display : true,
        			labelString : 'Across the days/weeks/months'
        		}        	
            }],
            yAxes: [{
                type: 'logarithmic',

                scaleLabel :{
        			display : true,
        			labelString : 'Total Amount'
        		} 

            }]
        },
        legend: {
        	position : 'right'
        }
    }
});
</script>
<script type="text/javascript">
    var pltly = document.getElementById('myplot');
    var data = {{plt_data|safe}};
    var layout = {
      title:'Another version of Category chart',
      width: 1200,
      height: 400,
      xaxis : {
        automargin : true
      },
      yaxis : {
        tickprefix : '₹',
        tickformat:',.2f',
        type:'log',
        autorange : true
      }
    };
    Plotly.newPlot(pltly, data,layout);
</script>