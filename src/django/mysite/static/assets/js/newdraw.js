Chart.defaults.global.defaultFontFamily = 'Roboto, "Helvetica Neue", Arial, sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
Chart.defaults.global.defaultFontSize = 16;

const chartDrawFunctions = {
    "summary": {
        drawChart: drawCreditSummaryChart, 
    },
    "feature_importance": {
        drawChart: drawFeatureImportanceChart, 
    },
};

function fetchChartData(chartType) {
    return $.ajax({
        url: '/new_credit_data/',
        method: 'GET',
        success: function(data) {
            if (chartDrawFunctions[chartType]) {
                if (chartDrawFunctions[chartType].drawChart) {
                    chartDrawFunctions[chartType].drawChart(data[chartType]);
                }
            } else {
                console.error('Unknown chart type:', chartType);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error fetching data: ' + textStatus + ', ' + errorThrown);
        }
    });
}


function drawCreditSummaryChart(summaryData) {
    const ctx = document.getElementById('creditSummaryChart').getContext('2d');

    const labels = [
        "EBITDA마진",
        "EBITDA/금융비용",
        "부채비율",
        "순차입금의존도",
        "순차입금/EBITDA"
    ];

    // 데이터 추출 및 구성
    const companyValues = labels.map(label => summaryData.find(entry => entry.label_ko === label).current_year);
    const industryAvgValues = labels.map(label => summaryData.find(entry => entry.label_ko === label).industry_avg);

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '기업값',
                    data: companyValues,
                    backgroundColor: 'rgba(128, 0, 0, 0.8)',  
                },
                {
                    label: '산업평균',
                    data: industryAvgValues,
                    backgroundColor: 'rgba(0, 26, 51, 0.8)',  
                }
            ]
        },
        options: {
            scales: {
                x: {
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 6,
                        fontColor: '#333',
                        fontStyle: 'bold'
                    }
                },
                y: {
                    position: 'right',
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        beginAtZero: true,
                    }
                }
            },
            legend: {
                display: true,
                labels: {
                    fontColor: '#333',  // 진한 색
                    fontStyle: 'bold'   // 두껍게
                }
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
}

function drawFeatureImportanceChart(importanceData) {
    const ctx = document.getElementById('featureImportanceChart').getContext('2d');

    const labels = ["자산총계", "자본총계", "당좌자산", "시가총액", "매출액"];

    const companyValues = labels.map(label => importanceData.find(entry => entry.label_ko === label).current_year / 100000000);
    const industryAvgValues = labels.map(label => importanceData.find(entry => entry.label_ko === label).industry_avg / 100000000);

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '기업값',
                    data: companyValues,
                    backgroundColor: 'rgba(128, 0, 0, 0.8)',  
                },
                {
                    label: '산업평균',
                    data: industryAvgValues,
                    backgroundColor: 'rgba(0, 26, 51, 0.8)',  
                }
            ]
        },
        options: {
            scales: {
                x: {
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 6,
                        fontColor: '#333',
                        fontStyle: 'bold'
                    }
                },
                y: {
                    position: 'right',
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) {
                            return value.toFixed(1); // if needed you can add "억" here
                        }
                    }
                }
            },
            legend: {
                display: true,
                labels: {
                    fontColor: '#333',
                    fontStyle: 'bold'
                }
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
                        // Since we've divided by 100 million for plotting, multiply it back for display in tooltip.
                        label += (tooltipItem.yLabel * 100000000).toFixed(1)
                        return label;
                    }
                }
            }
        }
    });
}








$(document).ready(function() {
    fetchChartData('summary');
    fetchChartData('feature_importance');
});
