Highcharts.chart('container1', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Popularidad de los deportes'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f}%'
            }
        }
    },
    series: [{
        name: 'Cantidad de hinchas',
        data: []
    }]
});

Highcharts.chart('container2', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Popularidad de las artesanias'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f}%'
            }
        }
    },
    series: [{
        name: 'Cantidad de artesanos',
        data: []
    }]
});

fetch("http://127.0.0.1:5000/get-estadistica-data-hincha")
    .then((response) => response.json())
    .then((data) =>{
        let parsedData = data.map((item) => {
            return [
                item.name,
                item.count,
            ];
        });

        const chart = Highcharts.charts.find(
            (chart) => chart && chart.renderTo.id === "container1"
        );

        chart.update({
            series: [
                {
                    data: parsedData,
                },
            ],
        });
    })
    .catch((error) => console.error("Error: ", error));

fetch("http://127.0.0.1:5000/get-estadistica-data-artesano")
    .then((response) => response.json())
    .then((data) =>{
        let parsedData = data.map((item) => {
            return [
                item.name,
                item.count,
            ];
        });

        const chart = Highcharts.charts.find(
            (chart) => chart && chart.renderTo.id === "container2"
        );

        chart.update({
            series: [
                {
                    data: parsedData,
                },
            ],
        });
    })
    .catch((error) => console.error("Error: ", error));