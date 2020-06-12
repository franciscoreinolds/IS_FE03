<template>
    <line-chart 
      class = "charterino"
      :styles="myStyles"
      :chart-data="data"
      :options="my_options"
    >
    </line-chart>
</template>

<script>
  import LineChart from '../LineChart.js'

  export default {
    components: {
      LineChart
    },
    data () {
      return {
        datacollection: null,
        myStyles: {
          height: '300px',
        },
        options : {
          legend: {
              position: 'bottom',
              },
              scales: {
                  yAxes: [{
                      display: true,
                      ticks: {
                          beginAtZero: true,
                          steps: 20,
                          stepValue: 10,
                          max: 50
                      }
                  }]
              },
              tooltips: {
              },
              height: 300,
              maintainAspectRatio: false,
              responsive: true
          }
      }
    },
    mounted () {
      this.fillData()
    },
    methods: {
      fillData () {
        this.datacollection = {
          labels: [2018,2019,2020],
          datasets: [
            {
              label : 'Citações',
              backgroundColor : '#f87979',
              data : [13,15,24],
            }
          ]
        }
      },
    },
    props : [
      'data',
      'my_options'
    ]
  }
</script>

<style>
  .small {
    width: 100%;
    height: 300px;
    margin: 25px auto;
    justify-content: center;
  }

  .charterino {
    margin: 0 auto;
  }
</style>
