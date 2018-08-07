var x_values = new Array(60)
var frequencies = new Array(60)

for (var i = 1; i <= 60; i++) {
    x_values[i - 1] = Math.floor(Math.random() * (60 - 0 + 1)) + 0;
    frequencies[i - 1] = i
}


Highcharts.chart('fft1', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Channel 1 Frequency Amplitudes'
    },
    xAxis: {
        categories: frequencies
    },
    yAxis: {
        title: {
            text: 'Amplitude (uV)'
        }
    },
    credits: {
        enabled: false
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Channel 1',
        data: x_values
    }]
});


Highcharts.chart('fft2', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Channel 2 Frequency Amplitudes'
    },
    xAxis: {
        categories: frequencies
    },
    yAxis: {
        title: {
            text: 'Amplitude (uV)'
        }
    },
    credits: {
        enabled: false
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Channel 2',
        color: '#ff5e5e',
        data: x_values
    }]
});


Highcharts.chart('fft3', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Channel 3 Frequency Amplitudes'
    },
    xAxis: {
        categories: frequencies
    },
    yAxis: {
        title: {
            text: 'Amplitude (uV)'
        }
    },
    credits: {
        enabled: false
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Channel 3',
        color: '#5eff86',
        data: x_values
    }]
});


Highcharts.chart('fft4', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Channel 4 Frequency Amplitudes'
    },
    xAxis: {
        categories: frequencies
    },
    yAxis: {
        title: {
            text: 'Amplitude (uV)'
        }
    },
    credits: {
        enabled: false
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Channel 4',
        color: '#f4ff68',
        data: x_values
    }]
});