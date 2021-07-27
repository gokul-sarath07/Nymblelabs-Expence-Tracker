const renderChart = (labels, data, chartId, heading) => {
  var ctx = document.getElementById(chartId).getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: labels,
          datasets: [{
              label: 'Current Months Expenses',
              data: data,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1
          }]
      },
      options: {
        plugins: {
          legend: {
            labels: {
              font: {
                size: 14
              }
            }
          },
          title: {
            display: true,
            text: heading,
            font: {
              size: 17
            }
          },
        },
      },
  });
};

// Function that updates the category amount.
const getChartDataForCategory = () => {
  fetch('/report/category-summery')
    .then(res => res.json())
    .then(result => {
      const category_data = result.expense_category_data
      const [labels, data] = [Object.keys(category_data), Object.values(category_data)]
      chartId = "myChartOne";
      heading = "Current Months Expenses per Category";
      renderChart(labels, data, chartId, heading);
    })
}

// Function that updates the weekly amount.
const getChartDataForWeekly = () => {
  fetch('/report/weekly-summery')
    .then(res => res.json())
    .then(result => {
      const weekly_data = result.expense_weekly_data
      const [labels, data] = [Object.keys(weekly_data), Object.values(weekly_data)]
      chartId = "myChartTwo";
      heading = "Current Months Expenses per Week";
      renderChart(labels, data, chartId, heading);
    })
}



document.onload = getChartDataForCategory();
document.onload = getChartDataForWeekly();
