<template>
	<div>
		<h1>
			Gráficos
		</h1>
		<h3>
			Tempo de Recolha das Publicações em Tempo Real
		</h3>
		<br>
        <Charts
            v-if="display_graph"
            v-bind:data="rtime_pub_collection"
            v-bind:my_options="rtime_pub_options"
        />
        <br>
        <div
        class = "chart"
        >
            <Charts
                v-if="display_graph"
                v-bind:data="rtime_pub_avg_collection"
                v-bind:my_options="rtime_pub_avg_options"
            />
        </div>
        <br>
        <!---->
        <h3>
			Tempo de Inserção das Publicações em Backoffice
		</h3>
		<br>
		<Charts
			class = "charts"
            v-if="display_graph"
            v-bind:data="bo_publ_ins_collection"
            v-bind:my_options="bo_publ_ins_options"
        />
        <br>
        <Charts
            v-if="display_graph"
            v-bind:data="bo_publ_ins_avg_collection"
            v-bind:my_options="bo_publ_ins_avg_options"
        />
        <br>
        <!---->
        <h3>
			Tempo de Recolha das Publicações em Backoffice
		</h3>
		<br>
		<Charts
			class = "charts"
            v-if="display_graph"
            v-bind:data="bo_publ_get_collection"
            v-bind:my_options="bo_publ_get_options"
        />
        <br>
        <Charts
            v-if="display_graph"
            v-bind:data="bo_publ_get_avg_collection"
            v-bind:my_options="bo_publ_get_avg_options"
        />
        <br>
        <!---->
	</div>
</template>

<script>
	import citationsjson from '../citations.json';
	import Charts from './Charts.vue';
	import ChartAnnotationsPlugin from 'chartjs-plugin-annotation';

	export default {
	 	name : "Graphs",
	    components : {
	        Charts
	    },
	    data () {
	        return {
	        	display_graph : false,
	            rtime_pub_collection : {
	                labels: [],
	                datasets: [
	                    {
	                    label : 'Publicações recuperadas',
	                    yAxesID : 'A',
	                    backgroundColor : '#f87979',
	                    data : [],
	                    },
	                    {
	                    label : 'Tempo para recuperar publicações ( em ms )',
	                    yAxesID : 'B',
	                    backgroundColor : '#D099D1',
	                    data : [],
	                    }
	                ]
	            },
	            rtime_pub_options : {},
	            rtime_pub_avg_collection : {
	                labels: [],
	                datasets: [
	                    {
	                    label : 'Tempo por Publicação Recuperada ( em ms )',
	                    yAxesID : 'C',
	                    backgroundColor : '#3ADF00',
	                    data : [],
	                    },
	                ],
	            },
	            rtime_pub_avg_options : {},
	            bo_publ_ins_collection : {
	            	labels: [],
	                datasets: [
	                    {
	                    label : 'Publicações recuperadas',
	                    yAxesID : 'A',
	                    backgroundColor : '#f87979',
	                    data : [],
	                    },
	                    {
	                    label : 'Tempo para recuperar publicações ( em ms )',
	                    yAxesID : 'B',
	                    backgroundColor : '#D099D1',
	                    data : [],
	                    }
	                ]	
	            },
	            bo_publ_ins_options : {},
	            bo_publ_ins_avg_collection : {
	            	labels: [],
	                datasets: [
	                    {
	                    label : 'Tempo por Publicação Recuperada ( em ms )',
	                    yAxesID : 'C',
	                    backgroundColor : '#3ADF00',
	                    data : [],
	                    },
	                ],
	            },
	            bo_publ_ins_avg_options : {},
	            bo_publ_get_collection : {
	            	labels: [],
	                datasets: [
	                    {
	                    label : 'Publicações recuperadas',
	                    yAxesID : 'A',
	                    backgroundColor : '#f87979',
	                    data : [],
	                    },
	                    {
	                    label : 'Tempo para recuperar publicações ( em ms )',
	                    yAxesID : 'B',
	                    backgroundColor : '#D099D1',
	                    data : [],
	                    }
	                ]	
	            },
	            bo_publ_get_options : {},
	            bo_publ_get_avg_collection : {
	            	labels: [],
	                datasets: [
	                    {
	                    label : 'Tempo por Publicação Recuperada ( em ms )',
	                    yAxesID : 'C',
	                    backgroundColor : '#3ADF00',
	                    data : [],
	                    },
	                ],
	            },
	            bo_publ_get_avg_options : {}
	        }
	    },
	    async created () {
	    	var rec_res = await fetch('http://localhost:5000/records', {headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}})
            
            var rec_data = await rec_res.json()

            var avg_time = 0

            var total_avg_time = 0

            for (var it = 0 ; it < rec_data['records'].length ; it++) {
                var rec = rec_data['records'][it]
                this.rtime_pub_collection.labels.push(rec['id'])
                this.rtime_pub_avg_collection.labels.push(rec['id'])
                
                this.rtime_pub_collection.datasets[0].data.push(rec['fetched_records'])
                this.rtime_pub_collection.datasets[1].data.push(rec['fetch_time'])
                this.rtime_pub_avg_collection.datasets[0].data.push(rec['fetch_time'] / rec['fetched_records'])

                total_avg_time += rec['fetch_time']
                avg_time += (rec['fetch_time'] / rec['fetched_records'])
                //console.log(rec)
            }

            total_avg_time /= this.rtime_pub_collection.datasets[1].data.length
            avg_time /= this.rtime_pub_avg_collection.datasets[0].data.length

            var most_records = Math.max.apply(Math, this.rtime_pub_collection.datasets[0].data)

            var longest_time = Math.max.apply(Math, this.rtime_pub_collection.datasets[1].data)

            // feed Real Time Publication settings
            // Real Time Publication Options
            this.rtime_pub_options = {
                legend: {
                    position: 'bottom',
                },
                scales: {
                    yAxes: [
                        {
                            id : 'A',
                            type: 'linear',
                            position: 'left',
                            ticks: {
                                beginAtZero: true,
                                fontColor : '#f87979'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Publicações Recuperadas',
                                fontColor: '#f87979',
                                fontSize:10
                            },
                            gridLines : {
                                display : false
                            }
                        },
                        {
                            id : 'B',
                            position: 'right',
                            type: 'linear',
                            ticks: {
                                beginAtZero: true,
                                max : longest_time,
                                min : 0,
                                fontColor : '#D099D1'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Tempo para Recuperar Publicações ( em ms )',
                                fontColor:'#D099D1',
                                fontSize:10
                            },
                            gridLines : {
                                display : true
                            }
                        }
                    ]
                },
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'A',
                            value: total_avg_time,
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 4,
                            label: {
                                enabled: true,
                                content: 'Tempo médio = ' + Math.round(total_avg_time*100)/100 + ' (ms)',
                                backgroundColor: 'rgba(0,0,0,0.3)',
                            }
                        }
                    ]
                },
                height: 300,
                maintainAspectRatio: false,
                responsive: true
            }

            // Real Time Publication Average Options
            this.rtime_pub_avg_options = {
                legend: {
                    position: 'bottom',
                },
                scales: {
                    yAxes: [
                        {
                            id : 'C',
                            type: 'linear',
                            position: 'left',
                            ticks: {
                                beginAtZero: true,
                                fontColor : '#3ADF00'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Tempo por Publicação Recuperada ( em ms )',
                                fontColor: '#3ADF00',
                                fontSize:10
                            },
                            gridLines : {
                                display : false
                            }
                        },
                    ]
                },
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'C',
                            value: avg_time,
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 4,
                            label: {
                                enabled : true,
                                content: 'Tempo médio = ' + Math.round(avg_time*100)/100 + ' (ms)',
                                backgroundColor: 'rgba(0,0,0,0.3)',
                            },
                        }
                    ]
                },
                height: 300,
                maintainAspectRatio: false,
                responsive: true
            }

            // Backoffice Publication Insert

            var bo_publ_ins_response = await fetch('http://localhost:5000/bo_publ_insert', {headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}})
            
            var bo_publ_ins_data = await bo_publ_ins_response.json()
            
            avg_time = 0

            total_avg_time = 0

            console.log(bo_publ_ins_data)

            for (var it = 0 ; it < bo_publ_ins_data['records'].length ; it++) {
                var rec = bo_publ_ins_data['records'][it]
                this.bo_publ_ins_collection.labels.push(rec['id'])
                this.bo_publ_ins_avg_collection.labels.push(rec['id'])
                
                this.bo_publ_ins_collection.datasets[0].data.push(rec['fetched_records'])
                this.bo_publ_ins_collection.datasets[1].data.push(rec['fetch_time'])
                this.bo_publ_ins_avg_collection.datasets[0].data.push(rec['fetch_time'] / rec['fetched_records'])

                total_avg_time += rec['fetch_time']
                avg_time += (rec['fetch_time'] / rec['fetched_records'])
            }

            total_avg_time /= this.bo_publ_ins_collection.datasets[1].data.length
            avg_time /= this.bo_publ_ins_avg_collection.datasets[0].data.length

            most_records = Math.max.apply(Math, this.bo_publ_ins_collection.datasets[0].data)

            longest_time = Math.max.apply(Math, this.bo_publ_ins_collection.datasets[1].data)

            // Backoffice Publication Insertion
            this.bo_publ_ins_options = {
                legend: {
                    position: 'bottom',
                },
                scales: {
                    yAxes: [
                        {
                            id : 'A',
                            type: 'linear',
                            position: 'left',
                            ticks: {
                                beginAtZero: true,
                                fontColor : '#f87979'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Publicações Recuperadas',
                                fontColor: '#f87979',
                                fontSize:10
                            },
                            gridLines : {
                                display : false
                            }
                        },
                        {
                            id : 'B',
                            position: 'right',
                            type: 'linear',
                            ticks: {
                                beginAtZero: true,
                                max : longest_time,
                                min : 0,
                                fontColor : '#D099D1'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Tempo para Recuperar Publicações ( em s )',
                                fontColor:'#D099D1',
                                fontSize:10
                            },
                            gridLines : {
                                display : true
                            }
                        }
                    ]
                },
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'A',
                            value: total_avg_time,
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 4,
                            label: {
                                enabled: true,
                                content: 'Tempo médio = ' + Math.round(total_avg_time*100)/100 + ' (s)',
                                backgroundColor: 'rgba(0,0,0,0.3)',
                            }
                        }
                    ]
                },
                height: 300,
                maintainAspectRatio: false,
                responsive: true
            }


            // Backoffice Publication Insert Average Options
            this.bo_publ_ins_avg_options = {
                legend: {
                    position: 'bottom',
                },
                scales: {
                    yAxes: [
                        {
                            id : 'C',
                            type: 'linear',
                            position: 'left',
                            ticks: {
                                beginAtZero: true,
                                fontColor : '#3ADF00'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Tempo por Publicação Recuperada ( em s )',
                                fontColor: '#3ADF00',
                                fontSize:10
                            },
                            gridLines : {
                                display : false
                            }
                        },
                    ]
                },
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'C',
                            value: avg_time,
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 4,
                            label: {
                                enabled : true,
                                content: 'Tempo médio = ' + Math.round(avg_time*100)/100 + ' (s)',
                                backgroundColor: 'rgba(0,0,0,0.3)',
                            },
                        }
                    ]
                },
                height: 300,
                maintainAspectRatio: false,
                responsive: true
            }

            // Backoffice Publication Get

            var bo_publ_get_response = await fetch('http://localhost:5000/bo_publ_get', {headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}})
            
            var bo_publ_get_data = await bo_publ_get_response.json()
            
            avg_time = 0

            total_avg_time = 0

            console.log(bo_publ_get_data)

            for (var it = 0 ; it < bo_publ_get_data['records'].length ; it++) {
                var rec = bo_publ_get_data['records'][it]
                this.bo_publ_get_collection.labels.push(rec['id'])
                this.bo_publ_get_avg_collection.labels.push(rec['id'])
                
                this.bo_publ_get_collection.datasets[0].data.push(rec['fetched_records'])
                this.bo_publ_get_collection.datasets[1].data.push(rec['fetch_time'])
                this.bo_publ_get_avg_collection.datasets[0].data.push(rec['fetch_time'] / rec['fetched_records'])

                total_avg_time += rec['fetch_time']
                avg_time += (rec['fetch_time'] / rec['fetched_records'])
            }

            total_avg_time /= this.bo_publ_get_collection.datasets[1].data.length
            avg_time /= this.bo_publ_get_avg_collection.datasets[0].data.length

            most_records = Math.max.apply(Math, this.bo_publ_get_collection.datasets[0].data)

            longest_time = Math.max.apply(Math, this.bo_publ_get_collection.datasets[1].data)

            // Backoffice Publication Insertion
            this.bo_publ_get_options = {
                legend: {
                    position: 'bottom',
                },
                scales: {
                    yAxes: [
                        {
                            id : 'A',
                            type: 'linear',
                            position: 'left',
                            ticks: {
                                beginAtZero: true,
                                fontColor : '#f87979'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Publicações Recuperadas',
                                fontColor: '#f87979',
                                fontSize:10
                            },
                            gridLines : {
                                display : false
                            }
                        },
                        {
                            id : 'B',
                            position: 'right',
                            type: 'linear',
                            ticks: {
                                beginAtZero: true,
                                max : longest_time,
                                min : 0,
                                fontColor : '#D099D1'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Tempo para Recuperar Publicações ( em ms )',
                                fontColor:'#D099D1',
                                fontSize:10
                            },
                            gridLines : {
                                display : true
                            }
                        }
                    ]
                },
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'A',
                            value: total_avg_time,
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 4,
                            label: {
                                enabled: true,
                                content: 'Tempo médio = ' + Math.round(total_avg_time*100)/100 + ' (ms)',
                                backgroundColor: 'rgba(0,0,0,0.3)',
                            }
                        }
                    ]
                },
                height: 300,
                maintainAspectRatio: false,
                responsive: true
            }


            // Backoffice Publication Insert Average Options
            this.bo_publ_get_avg_options = {
                legend: {
                    position: 'bottom',
                },
                scales: {
                    yAxes: [
                        {
                            id : 'C',
                            type: 'linear',
                            position: 'left',
                            ticks: {
                                beginAtZero: true,
                                fontColor : '#3ADF00'
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Tempo por Publicação Recuperada ( em ms )',
                                fontColor: '#3ADF00',
                                fontSize:10
                            },
                            gridLines : {
                                display : false
                            }
                        },
                    ]
                },
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'horizontal',
                            scaleID: 'C',
                            value: avg_time,
                            borderColor: 'rgb(75, 192, 192)',
                            borderWidth: 4,
                            label: {
                                enabled : true,
                                content: 'Tempo médio = ' + Math.round(avg_time*100)/100 + ' (ms)',
                                backgroundColor: 'rgba(0,0,0,0.3)',
                            },
                        }
                    ]
                },
                height: 300,
                maintainAspectRatio: false,
                responsive: true
            }

            this.display_graph = true;
	    }
	}
</script>

<style>

.progress {
	margin: 0 auto;
    justify-content: center;
}


.card_holder {
    padding-bottom : 2px;
}

.card {
    max-height : 800px;
    width : 90%;
    overflow-y: auto;
    justify-content: center;
}

.citations {
    justify-content: center;
    width : '85%'
}

.center-card-text {
    text-align : left;
}

.source_text {
    vertical-align: text-bottom;
}

.quartiles {
    justify-content: center;
}

.chart_row {
    display : flex;
}

.chart_col {
    text-align : center;
    flex : 50%;
    padding : 10px;
}

.chart {
    width : '50%'
}

</style>