Chart.defaults.global.defaultFontFamily = 'Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
Chart.defaults.global.defaultFontSize = 16;

function fetchChartData(company_name, chart_type) {
    return $.ajax({
        url: '/chart_data/' + chart_type + '/',
        method: 'GET',
        data: {
            company_name: company_name
        },
        success: function(data) {
            if (chart_type === 'profitability_indicator') {
                drawProfitabilityIndicatorChart(data);
            } else if (chart_type === 'return_investment') {
                drawReturnInvestmentChart(data);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error fetching data: ' + textStatus + ', ' + errorThrown);
        }
    });
}

function drawProfitabilityIndicatorChart(data) {
    var labels = ["2018", "2019", "2020", "2021", "2022"];
    var salesData = [];
    var profitMarginData = [];
    var netProfitMarginData = [];

    var salesItem = data.sales[0];
    salesData.push(salesItem.number_2018 / 100000000);
    salesData.push(salesItem.number_2019 / 100000000);
    salesData.push(salesItem.number_2020 / 100000000);
    salesData.push(salesItem.number_2021 / 100000000);
    salesData.push(salesItem.number_2022 / 100000000);

    var profitMarginItem = data.profit_margin[0];
    profitMarginData.push(profitMarginItem.number_2018);
    profitMarginData.push(profitMarginItem.number_2019);
    profitMarginData.push(profitMarginItem.number_2020);
    profitMarginData.push(profitMarginItem.number_2021);
    profitMarginData.push(profitMarginItem.number_2022);

    var netProfitMarginItem = data.net_profit_margin[0];
    netProfitMarginData.push(netProfitMarginItem.number_2018);
    netProfitMarginData.push(netProfitMarginItem.number_2019);
    netProfitMarginData.push(netProfitMarginItem.number_2020);
    netProfitMarginData.push(netProfitMarginItem.number_2021);
    netProfitMarginData.push(netProfitMarginItem.number_2022);

    var ctx = document.getElementById('profitability_indicator');
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "영업이익률",
                    backgroundColor: "rgba(214, 69, 65, 0.5)", // 어두운 핑크
                    borderColor: "rgba(214, 69, 65, 1)", // 경계 색상
                    borderWidth: 2, // 경계 두께
                    data: profitMarginData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 7,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "순이익률",
                    backgroundColor: "rgba(125, 60, 152, 0.5)", // 어두운 보라
                    borderColor: "rgba(125, 60, 152, 1)", // 경계 색상
                    borderWidth: 2, // 경계 두께
                    data: netProfitMarginData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 7,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "매출액",
                    backgroundColor: "rgba(40, 80, 130, 0.6)", // 어두운 초록색 (투명도 증가)
                    borderColor: "rgba(40, 80, 130, 1)", // 경계 색상
                    borderWidth: 2, // 경계 두께
                    data: salesData,
                    yAxisID: 'y-axis-1'
                }
            ],
        },
        options: {
            scales: {
                xAxes: [{
                    time: {
                        unit: 'year'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    }
                }],
                yAxes: [{
                    id: 'y-axis-1',
                    ticks: {
                        min: 0,
                        maxTicksLimit: 5
                    },
                    gridLines: {
                        display: true
                    }
                },
                {
                    id: 'y-axis-2',
                    position: 'right',
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        min: 0,
                        max: 100
                    }
                }],
            },
            legend: {
                display: true
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.yLabel.toFixed(1);
                        return label;
                    }
                }
            }
        }
    });
};

function drawReturnInvestmentChart(data) {
    var labels = ["2018", "2019", "2020", "2021", "2022"];
    var netIncomeData = [];
    var roeData = [];
    var roaData = [];
    var roicData = [];

    var netIncomeItem = data.net_income[0];
    netIncomeData.push(netIncomeItem.number_2018 / 100000000);
    netIncomeData.push(netIncomeItem.number_2019 / 100000000);
    netIncomeData.push(netIncomeItem.number_2020 / 100000000);
    netIncomeData.push(netIncomeItem.number_2021 / 100000000);
    netIncomeData.push(netIncomeItem.number_2022 / 100000000);

    var roeItem = data.roe[0];
    roeData.push(roeItem.number_2018);
    roeData.push(roeItem.number_2019);
    roeData.push(roeItem.number_2020);
    roeData.push(roeItem.number_2021);
    roeData.push(roeItem.number_2022);

    var roaItem = data.roa[0];
    roaData.push(roaItem.number_2018);
    roaData.push(roaItem.number_2019);
    roaData.push(roaItem.number_2020);
    roaData.push(roaItem.number_2021);
    roaData.push(roaItem.number_2022);

    var roicItem = data.roic[0];
    roicData.push(roicItem.number_2018);
    roicData.push(roicItem.number_2019);
    roicData.push(roicItem.number_2020);
    roicData.push(roicItem.number_2021);
    roicData.push(roicItem.number_2022);

    var ctx = document.getElementById('return_investment');
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "ROE",
                    backgroundColor: "transparent",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 2,
                    data: roeData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 7,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "ROA",
                    backgroundColor: "transparent",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 2,
                    data: roaData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 7,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "ROIC",
                    backgroundColor: "transparent",
                    borderColor: "rgba(255, 206, 86, 1)",
                    borderWidth: 2,
                    data: roicData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 7,
                    pointStyle: 'circle',
                    lineTension: 0
                },
                {
                    label: "당기순이익",
                    backgroundColor: "rgba(54, 162, 235, 0.6)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 2,
                    data: netIncomeData,
                    yAxisID: 'y-axis-1'
                }
            ],
        },
        options: {
            scales: {
                xAxes: [{
                    time: {
                        unit: 'year'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    }
                }],
                yAxes: [{
                    id: 'y-axis-1',
                    ticks: {
                        beginAtZero: true,
                        maxTicksLimit: 5
                    },
                    gridLines: {
                        display: true
                    }
                },
                {
                    id: 'y-axis-2',
                    position: 'right',
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        beginAtZero: true,
                        max: 100
                    }
                }],
            },
            legend: {
                display: true
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.yLabel.toFixed(1);
                        return label;
                    }
                }
            }
        }
    });
};

$(document).ready(function() {
    fetchChartData(corp, 'profitability_indicator');
    fetchChartData(corp, 'return_investment');
});


