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
                drawProfitabilityIndicatorTable(data);
            } else if (chart_type === 'return_investment') {
                drawReturnInvestmentChart(data);
                drawReturnInvestmentTable(data);
            } else if (chart_type === 'profitability_growth') {
                drawProfitabilityGrowthChart(data);
                drawProfitabilityGrowthTable(data);
            } else if (chart_type === 'asset_growth') {
                drawAssetGrowthChart(data);
                drawAssetGrowthTable(data);
            } else if (chart_type === 'stability') {
                drawStabilityChart(data);
                drawStabilityTable(data);
            } else if (chart_type === 'turnover') {
                drawTurnoverChart(data);
                drawTurnoverTable(data);
            } else if (chart_type === 'per_share') {
                drawPerShareChart(data); 
                drawPerShareTable(data); 
            } else if (chart_type === 'value') {
                drawValueChart(data); 
                drawValueTable(data); 
            } else if (chart_type === 'industry') {
                drawIndustryChart(data);
                drawIndustryTable(data); 
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error fetching data: ' + textStatus + ', ' + errorThrown);
        }
    });
}

function drawProfitabilityIndicatorChart(data) {
    const labels = ["2018", "2019", "2020", "2021", "2022"];
    const salesData = [];
    const profitMarginData = [];
    const netProfitMarginData = [];

    const salesItem = data.sales[0];
    salesData.push(salesItem.number_2018 / 100000000);
    salesData.push(salesItem.number_2019 / 100000000);
    salesData.push(salesItem.number_2020 / 100000000);
    salesData.push(salesItem.number_2021 / 100000000);
    salesData.push(salesItem.number_2022 / 100000000);

    const profitMarginItem = data.profit_margin[0];
    profitMarginData.push(profitMarginItem.number_2018);
    profitMarginData.push(profitMarginItem.number_2019);
    profitMarginData.push(profitMarginItem.number_2020);
    profitMarginData.push(profitMarginItem.number_2021);
    profitMarginData.push(profitMarginItem.number_2022);

    const netProfitMarginItem = data.net_profit_margin[0];
    netProfitMarginData.push(netProfitMarginItem.number_2018);
    netProfitMarginData.push(netProfitMarginItem.number_2019);
    netProfitMarginData.push(netProfitMarginItem.number_2020);
    netProfitMarginData.push(netProfitMarginItem.number_2021);
    netProfitMarginData.push(netProfitMarginItem.number_2022);

    const ctx = document.getElementById('profitability_indicator');
    const myLineChart = new Chart(ctx, {
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
    const labels = ["2018", "2019", "2020", "2021", "2022"];
    const netIncomeData = [];
    const roeData = [];
    const roaData = [];
    const roicData = [];

    const netIncomeItem = data.net_income[0];
    netIncomeData.push(netIncomeItem.number_2018 / 100000000);
    netIncomeData.push(netIncomeItem.number_2019 / 100000000);
    netIncomeData.push(netIncomeItem.number_2020 / 100000000);
    netIncomeData.push(netIncomeItem.number_2021 / 100000000);
    netIncomeData.push(netIncomeItem.number_2022 / 100000000);

    const roeItem = data.roe[0];
    roeData.push(roeItem.number_2018);
    roeData.push(roeItem.number_2019);
    roeData.push(roeItem.number_2020);
    roeData.push(roeItem.number_2021);
    roeData.push(roeItem.number_2022);

    const roaItem = data.roa[0];
    roaData.push(roaItem.number_2018);
    roaData.push(roaItem.number_2019);
    roaData.push(roaItem.number_2020);
    roaData.push(roaItem.number_2021);
    roaData.push(roaItem.number_2022);

    const roicItem = data.roic[0];
    roicData.push(roicItem.number_2018);
    roicData.push(roicItem.number_2019);
    roicData.push(roicItem.number_2020);
    roicData.push(roicItem.number_2021);
    roicData.push(roicItem.number_2022);

    const ctx = document.getElementById('return_investment');
    const myLineChart = new Chart(ctx, {
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
    const labels = ["2019", "2020", "2021", "2022"];
    const revenue_growth_data = [];
    const operating_income_data = [];
    const netIncomeData = [];

    const revenueGrowthItem = data.revenue_growth[0];
    revenue_growth_data.push(revenueGrowthItem.number_2019 );
    revenue_growth_data.push(revenueGrowthItem.number_2020 );
    revenue_growth_data.push(revenueGrowthItem.number_2021 );
    revenue_growth_data.push(revenueGrowthItem.number_2022 );

    const operatingIncomeItem = data.operating_income[0];
    operating_income_data.push(operatingIncomeItem.number_2019);
    operating_income_data.push(operatingIncomeItem.number_2020);
    operating_income_data.push(operatingIncomeItem.number_2021);
    operating_income_data.push(operatingIncomeItem.number_2022);

    const netIncomeItem = data.net_income[0];
    netIncomeData.push(netIncomeItem.number_2019);
    netIncomeData.push(netIncomeItem.number_2020);
    netIncomeData.push(netIncomeItem.number_2021);
    netIncomeData.push(netIncomeItem.number_2022);

    const ctx = document.getElementById('profitability_growth');
    const myLineChart = new Chart(ctx, {
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
    const labels = ["2019", "2020", "2021", "2022"];
    const asset_growth_data = [];
    const tangible_asset_data = [];
    const total_equity_data = [];

    const assetGrowthItem = data.asset_growth[0];
    asset_growth_data.push(assetGrowthItem.number_2019 );
    asset_growth_data.push(assetGrowthItem.number_2020 );
    asset_growth_data.push(assetGrowthItem.number_2021 );
    asset_growth_data.push(assetGrowthItem.number_2022 );

    const tangibleAssetItem = data.tangible_asset[0];
    tangible_asset_data.push(tangibleAssetItem.number_2019);
    tangible_asset_data.push(tangibleAssetItem.number_2020);
    tangible_asset_data.push(tangibleAssetItem.number_2021);
    tangible_asset_data.push(tangibleAssetItem.number_2022);

    const totalEquityItem = data.total_equity[0];
    total_equity_data.push(totalEquityItem.number_2019);
    total_equity_data.push(totalEquityItem.number_2020);
    total_equity_data.push(totalEquityItem.number_2021);
    total_equity_data.push(totalEquityItem.number_2022);

    const ctx = document.getElementById('asset_growth');
    const myLineChart = new Chart(ctx, {
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
    const labels = ["2018", "2019", "2020", "2021", "2022"];
    const debt_data = [];
    const current_liabilities_data = [];
    const non_current_liabilities_data = [];

    const debtItem = data.debt[0];
    debt_data.push(debtItem.number_2018 );
    debt_data.push(debtItem.number_2019 );
    debt_data.push(debtItem.number_2020 );
    debt_data.push(debtItem.number_2021 );
    debt_data.push(debtItem.number_2022 );

    const currentLiabilitiesItem = data.current_liabilities[0];
    current_liabilities_data.push(currentLiabilitiesItem.number_2018);
    current_liabilities_data.push(currentLiabilitiesItem.number_2019);
    current_liabilities_data.push(currentLiabilitiesItem.number_2020);
    current_liabilities_data.push(currentLiabilitiesItem.number_2021);
    current_liabilities_data.push(currentLiabilitiesItem.number_2022);

    const nonCurrentLiabilitiesItem = data.non_current_liabilities[0];
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2018);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2019);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2020);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2021);
    non_current_liabilities_data.push(nonCurrentLiabilitiesItem.number_2022);

    const ctx = document.getElementById('stability');
    const myLineChart = new Chart(ctx, {
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
    const labels = ["2018", "2019", "2020", "2021", "2022"];
    const asset_data = [];
    const accounts_receivable_data = [];
    const inventory_data = [];
    const accounts_payable_data = [];

    const assetItem = data.asset[0];
    asset_data.push(assetItem.number_2018 );
    asset_data.push(assetItem.number_2019 );
    asset_data.push(assetItem.number_2020 );
    asset_data.push(assetItem.number_2021 );
    asset_data.push(assetItem.number_2022 );

    const accountsReceivableItem = data.accounts_receivable[0];
    accounts_receivable_data.push(accountsReceivableItem.number_2018);
    accounts_receivable_data.push(accountsReceivableItem.number_2019);
    accounts_receivable_data.push(accountsReceivableItem.number_2020);
    accounts_receivable_data.push(accountsReceivableItem.number_2021);
    accounts_receivable_data.push(accountsReceivableItem.number_2022);

    const inventoryItem = data.inventory[0];
    inventory_data.push(inventoryItem.number_2018);
    inventory_data.push(inventoryItem.number_2019);
    inventory_data.push(inventoryItem.number_2020);
    inventory_data.push(inventoryItem.number_2021);
    inventory_data.push(inventoryItem.number_2022);

    const accountsPayableItem = data.accounts_payable[0];
    accounts_payable_data.push(accountsPayableItem.number_2018);
    accounts_payable_data.push(accountsPayableItem.number_2019);
    accounts_payable_data.push(accountsPayableItem.number_2020);
    accounts_payable_data.push(accountsPayableItem.number_2021);
    accounts_payable_data.push(accountsPayableItem.number_2022);

    const ctx = document.getElementById('turnover');
    const myLineChart = new Chart(ctx, {
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
    const labels = ["2018", "2019", "2020", "2021", "2022"];
    const eps_data = [];
    const bps_data = [];

    const epsItem = data.eps[0];
    eps_data.push(epsItem.number_2018 );
    eps_data.push(epsItem.number_2019 );
    eps_data.push(epsItem.number_2020 );
    eps_data.push(epsItem.number_2021 );
    eps_data.push(epsItem.number_2022 );

    const bpsItem = data.bps[0];
    bps_data.push(bpsItem.number_2018);
    bps_data.push(bpsItem.number_2019);
    bps_data.push(bpsItem.number_2020);
    bps_data.push(bpsItem.number_2021);
    bps_data.push(bpsItem.number_2022);

    const ctx = document.getElementById('per_share');
    const myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "EPS",
                    backgroundColor: "rgba(0, 51, 102, 0.6)",
                    borderColor: "rgba(0, 51, 102, 1)",
                    borderWidth: 1,
                    data: eps_data,
                    yAxisID: 'y-axis-1',
                },
                {
                    label: "BPS",
                    backgroundColor: "rgba(0, 76, 153, 0.6)",
                    borderColor: "rgba(0, 76, 153, 1)",
                    borderWidth: 1,
                    data: bps_data,
                    yAxisID: 'y-axis-1',
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

function drawValueChart(data) {
    const labels = ["2018", "2019", "2020", "2021", "2022"];
    const per_data = [];
    const pbr_data = [];
    const pcr_data = [];
  
    const perItem = data.per[0];
    per_data.push(perItem.number_2018 );
    per_data.push(perItem.number_2019 );
    per_data.push(perItem.number_2020 );
    per_data.push(perItem.number_2021 );
    per_data.push(perItem.number_2022 );
  
    const pbrItem = data.pbr[0];
    pbr_data.push(pbrItem.number_2018);
    pbr_data.push(pbrItem.number_2019);
    pbr_data.push(pbrItem.number_2020);
    pbr_data.push(pbrItem.number_2021);
    pbr_data.push(pbrItem.number_2022);
  
    const pcrItem = data.pcr[0];
    pcr_data.push(pcrItem.number_2018);
    pcr_data.push(pcrItem.number_2019);
    pcr_data.push(pcrItem.number_2020);
    pcr_data.push(pcrItem.number_2021);
    pcr_data.push(pcrItem.number_2022);
  
    const ctx = document.getElementById('value');
    const myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "PER",
                    backgroundColor: "transparent",
                    borderColor: "#8B0000",
                    borderWidth: 2,
                    data: per_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'rectRounded',
                    lineTension: 0
                },
                {
                    label: "PBR",
                    backgroundColor: "transparent",
                    borderColor: "#006363",
                    borderWidth: 2,
                    data: pbr_data,
                    yAxisID: 'y-axis-1',
                    fill: false,
                    pointRadius: 4,
                    pointStyle: 'triangle',
                    lineTension: 0
                },
                {
                    label: "PCR",
                    backgroundColor: "transparent",
                    borderColor: "#8B4500", 
                    borderWidth: 2,
                    data: pcr_data,
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

  function drawIndustryChart(data) {
    const ctx = document.getElementById('industry').getContext('2d');

    const chartData = {
        labels: ['수익성', '성장성', '안정성', '활동성', '가치지표'],
        datasets: [{
            label: data.company_name,
            data: [
                data.company.profitability,
                data.company.growth,
                data.company.stability,
                data.company.activity,
                data.company.valuation
            ],
            fill: true,
            backgroundColor: 'rgba(25, 40, 190, 0.5)', // 더 어두운 파랑색
            borderColor: 'rgba(25, 40, 190, 1)',
            pointBackgroundColor: 'rgba(25, 40, 190, 1)',
            pointHoverBorderColor: 'rgba(25, 40, 190, 1)'
        },
            {
            label: data.sector_name,
            data: [
                data.industry.profitability,
                data.industry.growth,
                data.industry.stability,
                data.industry.activity,
                data.industry.valuation
            ],
            fill: true,
            backgroundColor: 'rgba(180, 50, 40, 0.5)', // 더 어두운 주황색
            borderColor: 'rgba(180, 50, 40, 1)',
            pointBackgroundColor: 'rgba(180, 50, 40, 1)',
            pointHoverBorderColor: 'rgba(180, 50, 40, 1)'
        },]
    };

    const radarChart = new Chart(ctx, {
        type: 'radar',
        data: chartData,
        options: {
            scale: {
                ticks: {
                    display: false,
                    beginAtZero: true
                },
                pointLabels: {
                    fontSize: 18,    
                    fontStyle: "bold"  
                }
            },
            elements: {
                line: {
                    tension: 0,
                    borderWidth: 2
                },
                point: {
                    radius: 3,
                    hoverRadius: 7  
                }
            },
            tooltips: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                titleFontSize: 16,
                bodyFontSize: 14,
                xPadding: 10,
                yPadding: 10,
                displayColors: false,
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
            },
            legend: {
                position: 'bottom',
                labels: {
                    fontSize: 16,
                    fontStyle: "bold",
                    padding: 20
                }
            },
        }
    });
}


function drawProfitabilityIndicatorTable(data) {
    const tableBody = document.querySelector("#drawProfitabilityIndicatorTable tbody");
 
    const labelsInKorean = {
        "sales": "매출액",
        "profit_margin": "영업이익률",
        "net_profit_margin": "순이익률"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

 
        ["number_2018", "number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            
            if(label === "sales") {
                valueCell.textContent = (data[label][0][year] / 100000000).toFixed(1);
            } else {
                valueCell.textContent = data[label][0][year].toFixed(2);
            }
            
            row.appendChild(valueCell);
        }); 
        tableBody.appendChild(row);
    }
}

function drawReturnInvestmentTable(data) {
    const tableBody = document.querySelector("#drawReturnInvestmentTable tbody");

    const labelsInKorean = {
        "roe": "ROE",
        "roa": "ROA",
        "roic": "ROIC",
        "net_income": "당기순이익"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2018", "number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            
            if(label === "net_income") {
                valueCell.textContent = (data[label][0][year] / 100000000).toFixed(1); 
            } else {
                valueCell.textContent = data[label][0][year].toFixed(2); 
            }
            
            row.appendChild(valueCell);
        }); 

        tableBody.appendChild(row);
    }
}

function drawProfitabilityGrowthTable(data) {
    const tableBody = document.querySelector("#drawProfitabilityGrowthTable tbody");
 
    // 한국어 라벨 설정
    const labelsInKorean = {
        "revenue_growth": "매출액증가율",
        "operating_income": "영업이익증가율",
        "net_income": "순이익증가율"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            valueCell.textContent = data[label][0][year].toFixed(2);
            row.appendChild(valueCell);
        });

        tableBody.appendChild(row);
    }
}
function drawAssetGrowthTable(data) {
    const tableBody = document.querySelector("#drawAssetGrowthTable tbody");

    const labelsInKorean = {
        "asset_growth": "총자산증가율",
        "tangible_asset": "유형자산증가율",
        "total_equity": "자기자본증가율"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            valueCell.textContent = data[label][0][year].toFixed(2);
            row.appendChild(valueCell);
        });

        tableBody.appendChild(row);
    }
}
function drawStabilityTable(data) {
    const tableBody = document.querySelector("#drawStabilityTable tbody");

    const labelsInKorean = {
        "debt": "부채비율",
        "current_liabilities": "유동부채비율",
        "non_current_liabilities": "비유동부채비율"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2018", "number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            valueCell.textContent = data[label][0][year].toFixed(2);
            row.appendChild(valueCell);
        });

        tableBody.appendChild(row);
    }
}
function drawTurnoverTable(data) {
    const tableBody = document.querySelector("#drawTurnoverTable tbody");

    const labelsInKorean = {
        "asset": "총자산회전율",
        "accounts_receivable": "매출채권회전율",
        "inventory": "재고자산회전율",
        "accounts_payable": "매입채무회전율"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2018", "number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            valueCell.textContent = data[label][0][year].toFixed(2);
            row.appendChild(valueCell);
        });
        tableBody.appendChild(row);
    }
}
function drawPerShareTable(data) {
    const tableBody = document.querySelector("#drawPerShareTable tbody");
    const labelsInKorean = {
        "eps": "EPS",
        "bps": "BPS"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');

        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2018", "number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            valueCell.textContent = (data[label][0][year]).toFixed(2);

            row.appendChild(valueCell);
        });

        tableBody.appendChild(row);
    }
}
function drawValueTable(data) {
    const tableBody = document.querySelector("#drawValueTable tbody");
 
    const labelsInKorean = {
        "per": "PER",
        "pbr": "PBR",
        "pcr": "PCR"
    };

    for (let label in labelsInKorean) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = labelsInKorean[label];
        row.appendChild(nameCell);

        ["number_2018", "number_2019", "number_2020", "number_2021", "number_2022"].forEach(year => {
            const valueCell = document.createElement('td');
            valueCell.textContent = data[label][0][year].toFixed(2); 
            row.appendChild(valueCell);
        }); 
        tableBody.appendChild(row);
    }
}





function drawIndustryTable(data) {
    const tableBody = document.querySelector("#drawIndustryTable tbody");

    const categoriesInKorean = {
        "profitability": "수익성",
        "growth": "성장성",
        "stability": "안정성",
        "activity": "활동성",
        "valuation": "가치지표"
    };

    for (let category in categoriesInKorean) {
        const row = document.createElement('tr');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = categoriesInKorean[category];
        row.appendChild(nameCell);
        
        const companyCell = document.createElement('td');
        companyCell.textContent = (data.company[category]).toFixed(2);
        row.appendChild(companyCell);
        
        const industryCell = document.createElement('td');
        industryCell.textContent = (data.industry[category]).toFixed(2);
        row.appendChild(industryCell);
        
        tableBody.appendChild(row);
    }
}







$(document).ready(function() {
    fetchChartData(corp, 'profitability_indicator');
    fetchChartData(corp, 'return_investment');
    fetchChartData(corp, 'profitability_growth');
    fetchChartData(corp, 'asset_growth');
    fetchChartData(corp, 'stability');
    fetchChartData(corp, 'turnover');
    fetchChartData(corp, 'per_share');
    fetchChartData(corp, 'value');
    fetchChartData(corp, 'industry');
});


