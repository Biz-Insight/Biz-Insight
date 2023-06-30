// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';


// AJAX 요청을 보내고 응답
function fetchBarChartData(company_name) {
  return $.ajax({
      url: '/chart_data/',  // Django의 AJAX 뷰 URL
      method: 'GET',
      data: {
          company_name: company_name

      },
      success: function(data) {
          console.log(data);
          console.log('Data fetched successfully');
          drawBarChart(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
          console.error('Error fetching data: ' + textStatus + ', ' + errorThrown);
      }
  });
}



function drawBarChart(data) {
    var labels = ["2018", "2019", "2020", "2021", "2022"];
    var chartData = [];

    // JSON 응답을 파싱하고 차트 데이터를 추출.
    var item = data[0];
    chartData.push(item.number_2018 / 100000000);
    chartData.push(item.number_2019 / 100000000);
    chartData.push(item.number_2020 / 100000000);
    chartData.push(item.number_2021 / 100000000);
    chartData.push(item.number_2022 / 100000000);

    // console.log(item)
    // console.log(chartData)
    // console.log(item.number_2018)


    // 차트를 그리기
    var ctx = document.getElementById('myBarChart');
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "매출원가",
                backgroundColor: "rgba(2,117,216,1)",
                borderColor: "rgba(2,117,216,1)",
                data: chartData,
            }],
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
                    ticks: {
                        min: 0,
                        maxTicksLimit: 5
                    },
                    gridLines: {
                        display: true
                    }
                }],
            },
            legend: {
                display: false
            }
        }
    });
};

$(document).ready(function() {
    fetchBarChartData(company_name);
  });