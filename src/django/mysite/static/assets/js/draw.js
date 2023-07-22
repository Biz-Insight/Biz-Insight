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
            } else if (chart_type === 'profitability_growth') {
                drawProfitabilityGrowthChart(data);
            } else if (chart_type === 'asset_growth') {
                drawAssetGrowthChart(data);
            } else if (chart_type === 'stability') {
                drawStabilityChart(data);
            } else if (chart_type === 'turnover') {
                drawTurnoverChart(data);
            } else if (chart_type === 'per_share') {
                drawPerShareChart(data);
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
                    backgroundColor: "transparent",
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: profitMarginData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: 'origin',  
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "순이익률",
                    backgroundColor: "transparent",
                    borderColor:"#8B6508",
                    borderWidth: 2, 
                    data: netProfitMarginData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: 'origin',  
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "매출액",
                    backgroundColor: "rgba(0, 51, 102, 0.4)",
                    borderColor: "rgba(0, 51, 102, 1)", 
                    borderWidth: 2,
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
                        beginAtZero: true,
                        max : 100
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
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: roeData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "ROA",
                    backgroundColor: "transparent",
                    borderColor: "#006363", // Darker shade of teal/cyan
                    borderWidth: 2,
                    data: roaData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "ROIC",
                    backgroundColor: "transparent",
                    borderColor: "#8B6508", 
                    borderWidth: 2,
                    data: roicData,
                    yAxisID: 'y-axis-2',
                    type: 'line',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'circle',
                    lineTension: 0
                },
                {
                    label: "당기순이익",
                    backgroundColor: "rgba(0, 51, 102, 0.4)",
                    borderColor: "rgba(0, 51, 102, 1)", 
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

function drawProfitabilityGrowthChart(data) {
    var labels = ["2019", "2020", "2021", "2022"];
    var revenue_growth_data = [];
    var operating_income_data = [];
    var netIncomeData = [];

    var revenueGrowthItem = data.revenue_growth[0];
    revenue_growth_data.push(revenueGrowthItem.number_2019 );
    revenue_growth_data.push(revenueGrowthItem.number_2020 );
    revenue_growth_data.push(revenueGrowthItem.number_2021 );
    revenue_growth_data.push(revenueGrowthItem.number_2022 );

    var operatingIncomeItem = data.operating_income[0];
    operating_income_data.push(operatingIncomeItem.number_2019);
    operating_income_data.push(operatingIncomeItem.number_2020);
    operating_income_data.push(operatingIncomeItem.number_2021);
    operating_income_data.push(operatingIncomeItem.number_2022);

    var netIncomeItem = data.net_income[0];
    netIncomeData.push(netIncomeItem.number_2019);
    netIncomeData.push(netIncomeItem.number_2020);
    netIncomeData.push(netIncomeItem.number_2021);
    netIncomeData.push(netIncomeItem.number_2022);

    var ctx = document.getElementById('profitability_growth');
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "매출액증가율",
                    backgroundColor: "transparent",
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: revenue_growth_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "영업이익증가율",
                    backgroundColor: "transparent",
                    borderColor: "#006363",
                    borderWidth: 2,
                    data: operating_income_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "순이익증가율",
                    backgroundColor: "transparent",
                    borderColor: "#8B4500", 
                    borderWidth: 2,
                    data: netIncomeData,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'circle',
                    lineTension: 0
                },
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
                yAxes: [
                {
                    id: 'y-axis-1',
                    position: 'right',
                    gridLines: {
                        display: true
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

function drawAssetGrowthChart(data) {
    var labels = ["2019", "2020", "2021", "2022"];
    var asset_growth_data = [];
    var tangible_asset_data = [];
    var total_equity_data = [];

    var assetGrowthItem = data.asset_growth[0];
    asset_growth_data.push(assetGrowthItem.number_2019 );
    asset_growth_data.push(assetGrowthItem.number_2020 );
    asset_growth_data.push(assetGrowthItem.number_2021 );
    asset_growth_data.push(assetGrowthItem.number_2022 );

    var tangibleAssetItem = data.tangible_asset[0];
    tangible_asset_data.push(tangibleAssetItem.number_2019);
    tangible_asset_data.push(tangibleAssetItem.number_2020);
    tangible_asset_data.push(tangibleAssetItem.number_2021);
    tangible_asset_data.push(tangibleAssetItem.number_2022);

    var totalEquityItem = data.total_equity[0];
    total_equity_data.push(totalEquityItem.number_2019);
    total_equity_data.push(totalEquityItem.number_2020);
    total_equity_data.push(totalEquityItem.number_2021);
    total_equity_data.push(totalEquityItem.number_2022);

    var ctx = document.getElementById('asset_growth');
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "총자산증가율",
                    backgroundColor: "transparent",
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: asset_growth_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "유형자산증가율",
                    backgroundColor: "transparent",
                    borderColor: "#006363",
                    borderWidth: 2,
                    data: tangible_asset_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "자기자본증가율",
                    backgroundColor: "transparent",
                    borderColor: "#8B4500", 
                    borderWidth: 2,
                    data: total_equity_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'circle',
                    lineTension: 0
                },
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
                yAxes: [
                {
                    id: 'y-axis-1',
                    position: 'right',
                    gridLines: {
                        display: true
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


function drawStabilityChart(data) {
    var labels = ["2018", "2019", "2020", "2021", "2022"];
    var debt_data = [];
    var current_liabilities_data = [];
    var non_current_liabilities_data = [];

    var debtItem = data.debt[0];
    debt_data.push(debtItem.number_2018 );
    debt_data.push(debtItem.number_2019 );
    debt_data.push(debtItem.number_2020 );
    debt_data.push(debtItem.number_2021 );
    debt_data.push(debtItem.number_2022 );

    var currentLiabilitiesItem = data.current_liabilities[0];
    current_liabilities_data.push(currentLiabilitiesItem.number_2018);
    current_liabilities_data.push(currentLiabilitiesItem.number_2019);
    current_liabilities_data.push(currentLiabilitiesItem.number_2020);
    current_liabilities_data.push(currentLiabilitiesItem.number_2021);
    current_liabilities_data.push(currentLiabilitiesItem.number_2022);

    var nonCurrentLiabilitiesItem = data.non_current_liabilities[0];
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2018);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2019);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2020);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2021);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2022);

    var ctx = document.getElementById('stability');
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "부채비율",
                    backgroundColor: "transparent",
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: debt_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "유동부채비율",
                    backgroundColor: "transparent",
                    borderColor: "#006363",
                    borderWidth: 2,
                    data: current_liabilities_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "비유동부채비율",
                    backgroundColor: "transparent",
                    borderColor: "#8B4500", 
                    borderWidth: 2,
                    data: non_current_liabilities_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'circle',
                    lineTension: 0
                },
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
                yAxes: [
                {
                    id: 'y-axis-1',
                    position: 'right',
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        beginAtZero: true,
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

function drawTurnoverChart(data) {
    var labels = ["2018", "2019", "2020", "2021", "2022"];
    var asset_data = [];
    var accounts_receivable_data = [];
    var inventory_data = [];
    var accounts_payable_data = [];

    var assetItem = data.asset[0];
    asset_data.push(assetItem.number_2018 );
    asset_data.push(assetItem.number_2019 );
    asset_data.push(assetItem.number_2020 );
    asset_data.push(assetItem.number_2021 );
    asset_data.push(assetItem.number_2022 );

    var accountsReceivableItem = data.accounts_receivable[0];
    accounts_receivable_data.push(accountsReceivableItem.number_2018);
    accounts_receivable_data.push(accountsReceivableItem.number_2019);
    accounts_receivable_data.push(accountsReceivableItem.number_2020);
    accounts_receivable_data.push(accountsReceivableItem.number_2021);
    accounts_receivable_data.push(accountsReceivableItem.number_2022);

    var inventoryItem = data.inventory[0];
    inventory_data.push(inventoryItem.number_2018);
    inventory_data.push(inventoryItem.number_2019);
    inventory_data.push(inventoryItem.number_2020);
    inventory_data.push(inventoryItem.number_2021);
    inventory_data.push(inventoryItem.number_2022);

    var accountsPayableItem = data.accounts_payable[0];
    accounts_payable_data.push(accountsPayableItem.number_2018);
    accounts_payable_data.push(accountsPayableItem.number_2019);
    accounts_payable_data.push(accountsPayableItem.number_2020);
    accounts_payable_data.push(accountsPayableItem.number_2021);
    accounts_payable_data.push(accountsPayableItem.number_2022);

    var ctx = document.getElementById('turnover');
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "총자산회전율",
                    backgroundColor: "transparent",
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: asset_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "매출채권회전율",
                    backgroundColor: "transparent",
                    borderColor: "#006363",
                    borderWidth: 2,
                    data: accounts_receivable_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "재고자산회전율",
                    backgroundColor: "transparent",
                    borderColor: "#8B4500", 
                    borderWidth: 2,
                    data: inventory_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'circle',
                    lineTension: 0
                },
                {
                    label: "매입채무회전율",
                    backgroundColor: "transparent",
                    borderColor: "#8B4430", 
                    borderWidth: 2,
                    data: accounts_payable_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'square',
                    lineTension: 0
                },
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
                yAxes: [
                {
                    id: 'y-axis-1',
                    position: 'right',
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        beginAtZero: true,
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
function drawPerShareChart(data) {
    var labels = ["2018", "2019", "2020", "2021", "2022"];
    var per_data = [];
    var pbr_data = [];
    var pcr_data = [];

    var perItem = data.per[0];
    per_data.push(perItem.number_2018 );
    per_data.push(perItem.number_2019 );
    per_data.push(perItem.number_2020 );
    per_data.push(perItem.number_2021 );
    per_data.push(perItem.number_2022 );

    var pbrItem = data.pbr[0];
    pbr_data.push(pbrItem.number_2018);
    pbr_data.push(pbrItem.number_2019);
    pbr_data.push(pbrItem.number_2020);
    pbr_data.push(pbrItem.number_2021);
    pbr_data.push(pbrItem.number_2022);

    var pcrItem = data.pcr[0];
    pcr_data.push(pcrItem.number_2018);
    pcr_data.push(pcrItem.number_2019);
    pcr_data.push(pcrItem.number_2020);
    pcr_data.push(pcrItem.number_2021);
    pcr_data.push(pcrItem.number_2022);


    var ctx = document.getElementById('per_share');
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "PER",
                    backgroundColor: "rgba(0, 51, 102, 0.6)",
                    borderColor: "rgba(0, 51, 102, 1)",
                    borderWidth: 1,
                    data: per_data,
                    yAxisID: 'y-axis-1',
                },
                {
                    label: "PBR",
                    backgroundColor: "rgba(0, 76, 153, 0.6)",
                    borderColor: "rgba(0, 76, 153, 1)",
                    borderWidth: 1,
                    data: pbr_data,
                    yAxisID: 'y-axis-1',
                },
                {
                    label: "PCR",
                    backgroundColor: "rgba(0, 102, 204, 0.6)",
                    borderColor: "rgba(0, 102, 204, 1)",
                    borderWidth: 1,
                    data: pcr_data,
                    yAxisID: 'y-axis-1',
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
                yAxes: [
                {
                    id: 'y-axis-1',
                    position: 'right',
                    gridLines: {
                        display: true
                    },
                    ticks: {
                        beginAtZero: true,
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
    fetchChartData(corp, 'profitability_growth');
    fetchChartData(corp, 'asset_growth');
    fetchChartData(corp, 'stability');
    fetchChartData(corp, 'turnover');
    fetchChartData(corp, 'per_share');
});


