
const data = [  
    {    
        name: 'Portfolio',   
        data: [30, 40, 35, 50, 49, 60, 70, 91, 125, 130]
    },

    {
        name: 'Index',
        data: [20, 22, 30, 45, 60, 90, 105, 120, 135, 150]
    }
];

const options = {
  chart: {
    type: 'line',
    stacked: true,
    height: 350
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    width: [2, 2],
    curve: 'smooth'
  },
  series: data,
  xaxis: {
    type: 'datetime'
  },
  yaxis: {
    title: {
      text: 'Value'
    }
  },
  fill: {
    opacity: [0.8, 0.8],
    gradient: {
      inverseColors: false,
      shade: 'light',
      type: 'vertical',
      opacityFrom: 0.85,
      opacityTo: 0.55,
      stops: [0, 100]
    }
  },
  legend: {
    position: 'top',
    horizontalAlign: 'left',
    offsetX: 40
  }
};

const chart = new ApexCharts(document.querySelector('#chart'), options);


chart.render();
