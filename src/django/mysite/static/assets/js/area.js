// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// AJAX 요청을 보내고 응답
function fetchAreaChartData(company_name) {
  return $.ajax({
      url: '/stock_area/',  // Django의 AJAX 뷰 URL
      method: 'GET',
      data: {
          company_name: company_name
      },
      success: function(data) {
          console.log(data);
          console.log('Data fetched successfully');
          drawAreaChart(data);
      },
      error: function(jqXHR, textStatus, errorThrown) {
          console.error('Error fetching data: ' + textStatus + ', ' + errorThrown);
      }
  });
}

function drawAreaChart(data) {
  var labels = data.labels;
  var chartData = data.data;

  // Area Chart Example
  var ctx = document.getElementById("myAreaChart");
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: "주가",
        lineTension: 0.3,
        // backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 0.1,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(0,0,0,1)",
        pointHoverRadius: 1,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 500,
        pointBorderWidth: 2,
        data: chartData,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            maxTicksLimit: 50
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });
}

$(document).ready(function() {
  fetchAreaChartData(company_name);
});
