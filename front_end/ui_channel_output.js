var raw_chart1;  //global
var raw_chart2;  //global
var raw_chart3;  //global
var raw_chart4;  //global

Highcharts.setOptions({
    global: {
        useUTC: false
    },
    title: {
        style: {
            color: '#FFFFFF'
        }
    },
    xAxis: {
      labels: {
         style: {
            color: '#FFFFFF'
         }
      },
      title: {
         style: {
            color: 'FFFFFFF'
         }            
      }
    },
    yAxis: {
      labels: {
         style: {
            color: '#FFFFFF'
         }
      },
      title: {
         style: {
            color: '#FFFFFF'
         }            
      }
    },
    credits: {
        style: {
            display: 'none'
        }
    }
});

// CHANNEL 1
raw_chart1 = Highcharts.chart('channel1', {
    chart: {
        type: 'spline',
        zoomType: 'x',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {

                // set up the updating of the chart each second
                var series = this.series[0];
                setInterval(function () {
                    var x = (new Date()).getTime(), // current time
                        y = Math.random();
                    series.addPoint([x, y], true, true);
                }, 1000);
            }
        }
    },
    title: {
        text: 'Channel 1'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: 'Volt (uV)'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: 'Sample',
    }]
});


// CHANNEL 2
raw_chart2 = Highcharts.chart('channel2', {
    chart: {
        type: 'spline',
        zoomType: 'x',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {

                // set up the updating of the chart each second
                var series = this.series[0];
                setInterval(function () {
                    var x = (new Date()).getTime(), // current time
                        y = Math.random();
                    series.addPoint([x, y], true, true);
                }, 1000);
            }
        }
    },
    title: {
        text: 'Channel 2'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: 'Volt (uV)'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: 'Sample',
        color: '#ff5e5e',
    }]
});


// CHANNEL 3
raw_chart3 = Highcharts.chart('channel3', {
    chart: {
        type: 'spline',
        zoomType: 'x',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {

                // set up the updating of the chart each second
                var series = this.series[0];
                setInterval(function () {
                    var x = (new Date()).getTime(), // current time
                        y = Math.random();
                    series.addPoint([x, y], true, true);
                }, 1000);
            }
        }
    },
    title: {
        text: 'Channel 3'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: 'Volt (uV)'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: 'Sample',
        color: '#5eff86',
    }]
});


// CHANNEL 4
raw_chart4 = Highcharts.chart('channel4', {
    chart: {
        type: 'spline',
        zoomType: 'x',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {

                // set up the updating of the chart each second
                var series = this.series[0];
                setInterval(function () {
                    var x = (new Date()).getTime(), // current time
                        y = Math.random();
                    series.addPoint([x, y], true, true);
                }, 1000);
            }
        }
    },
    title: {
        text: 'Channel 4'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: 'Volt (uV)'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: 'Sample',
        color: '#f4ff68',
    }]
});


        //data: (function () {
            // generate an array of random data
            //var data = [],
                //time = (new Date()).getTime(),
                //i;

            //for (i = -19; i <= 0; i += 1) {
                //data.push({
                    //x: time + i * 1000,
                    //y: Math.random()
                //});
            //}
            //return data;
        //}())