<template>
    <div>
        <div
        v-if = "no_orcid">
            <h1>
                Não existe nenhum utilizador com o ORCID: {{this.orcid_id}}
            </h1>
        </div>
        <div
        v-else
        >   
            <h1>
            Informação sobre o/a Autor(a)
            </h1>
            <br>
            <v-card
            class = "card"
            >
                <v-card-title
                class = "center-card-text"
                >
                    {{this.author_info.name}}
                </v-card-title>
                <v-card-text>
                    <div
                    class = "center-card-text"
                    >
                        <h3>
                            Informações:
                        </h3>
                        <v-divider></v-divider>
                        <h4>
                            Orcid: {{this.author_info.orcid_id}}
                        </h4>
                        <h4>
                            Citações: {{this.author_info['citation-count']}}
                        </h4>
                        <h4>
                            Citado por: {{this.author_info['cited-by-count']}}
                        </h4>
                        <br>
                        <h3>
                            Áreas de Interesse:
                        </h3>
                        <v-divider></v-divider>
                        <br>
                        <div
                        class = "text-center"
                        >
                            <v-chip
                            class = "ma-2"
                            v-for="(subj, index) in this.author_info['subject-areas']"
                            :key="index"
                            >
                                {{subj}}
                            </v-chip>
                        </div>
                    </div>
                </v-card-text>
            </v-card>
            <br>
            <h1>
                Publicações
            </h1>
            <br>
            <v-card
            class = "card"
            >
                <v-card-title>
                    <v-text-field
                    v-model="search"
                    append-icon="mdi-search"
                    label="Filtrar por Título"
                    single-line
                    hide-details
                    ></v-text-field>
                </v-card-title>
                <v-progress-circular
                class = "progress"
                v-if="loading"
                :size="70"
                :width="7"
                color="blue-grey darken-4"
                indeterminate
                ></v-progress-circular>
                <v-data-table
                loading-text = "A carregar publicações"
                no-data-text = "Não existem publicações associadas ao OrcID fornecido"
                :headers = "headers"
                :items = "jsondata"
                :items-per-page = 10
                :search = "search"
                @click:row="handleClick"
                >
                </v-data-table>
            </v-card>
            <br>
            <v-dialog
            v-model="dialog"
            width="800"
            height="500"
            v-if="this.dialog == true"
            >
                <v-card>
                    <v-card-title>
                        {{this.selected_publishing.title}}
                    </v-card-title>
                    <v-card-text>
                        <div
                        class = "center-card-text"
                        >
                            <br>
                            <h3>
                                Publicação foi citada {{this.selected_publishing.citedby}} vez(es)
                            </h3>
                            <br>
                            <h3>
                                Data: {{this.selected_publishing.date}} | Tipo de Publicação: {{this.selected_publishing.type}}
                            </h3>
                            <v-divider></v-divider>
                            <h4
                            v-if="this.selected_publishing.wosuid"
                            >
                            WOSUID : {{this.selected_publishing.wosuid}}
                            </h4>
                            <div
                            >
                                <h4
                                v-if="this.selected_publishing.publishing_link != ''"
                                >
                                    <a
                                    style = "text-decoration:none; color:#555" 
                                    v-bind:href=this.selected_publishing.publishing_link
                                    >
                                        EID : {{this.selected_publishing.eid}}
                                    </a>
                                </h4>
                                <br>
                                <h3>
                                    Autores:
                                </h3>
                                <v-divider></v-divider>
                                <h4
                                v-for="(author_name, index) in this.selected_publishing.authors"
                                :key="index"
                                >
                                    {{author_name.given_name}} - ({{author_name.indexed_name}})
                                </h4>
                            </div>
                            <br>
                            <div
                            v-if = "this.selected_publishing.journal != null"
                            >
                                <br>
                                <h3>
                                    Informações do Local de Publicação
                                </h3>
                                <v-divider></v-divider>
                                <h4>
                                    Nome: {{this.selected_publishing.journal.title}}
                                </h4>
                                <h4>
                                    Publicante: {{this.selected_publishing.journal.publisher}}
                                </h4>
                                <h4
                                v-if="this.selected_publishing.journal.issn"
                                >
                                    ISSN: {{this.selected_publishing.journal.issn}}
                                </h4>
                                <h4
                                v-if="this.selected_publishing.journal.eissn"
                                >
                                    eISSN: {{this.selected_publishing.journal.eissn}}
                                </h4>
                                <h4>
                                    Início de Operação: {{this.selected_publishing.journal.start_year}}
                                </h4>
                                <h4
                                v-if="this.selected_publishing.journal.end_year != 2020 & this.selected_publishing.journal.end_year != null"
                                >
                                    Fim de Operação: {{this.selected_publishing.journal.end_year}}
                                </h4>
                                 <div
                                v-if="this.selected_publishing.journal.citescore"
                                >
                                    <br>
                                    <h4>
                                        CiteScore
                                    </h4>
                                    <v-simple-table>
                                          <thead>
                                            <tr>
                                              <th class="text-left">Ano</th>
                                              <th class="text-left">CiteScore</th>
                                            </tr>
                                          </thead>
                                          <tbody>
                                            <tr>
                                              <td> {{this.selected_publishing.journal.citescore.currentMetricYear}} </td>
                                              <td> {{this.selected_publishing.journal.citescore.currentMetric}} </td>
                                            </tr>
                                            <tr>
                                              <td> {{this.selected_publishing.journal.citescore.trackerYear}} </td>
                                              <td> {{this.selected_publishing.journal.citescore.tracker}} </td>
                                            </tr>
                                          </tbody>
                                      </v-simple-table>
                                    <br>
                                </div>
                                <div
                                    v-if="this.selected_publishing.journal.source_id"
                                    >
                                        <h4>
                                            Quartiles
                                        </h4>
                                        <a
                                            v-bind:href=this.selected_publishing.journal.quartiles_href
                                            title="SCImago Journal &amp; Country Rank"
                                        >
                                            <img
                                                border="0"
                                                v-bind:src=this.selected_publishing.journal.quartiles_src
                                                alt="SCImago Journal &amp; Country Rank"
                                            />
                                        </a>
                                    </div>
                                <div
                                v-if = "this.selected_publishing.journal.subject_areas"
                                >
                                    <h4>
                                        Temas:
                                    </h4>
                                    <v-chip
                                    class = "ma-2"
                                    v-for="(subj, index) in this.selected_publishing.journal.subject_areas"
                                    :key="index"
                                    >
                                        {{subj}}
                                    </v-chip>
                                </div>
                                <div
                                v-if="this.selected_publishing.journal.sjr"
                                >
                                    <br>
                                    <h4>
                                        Tabela de SJR
                                    </h4>
                                    <v-simple-table>
                                      <thead>
                                        <tr>
                                          <th class="text-left">Ano</th>
                                          <th class="text-left">SJR</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr
                                        v-for="(sjr, index) in this.selected_publishing.journal.sjr"
                                        :key="index"
                                        >
                                          <td>{{ sjr.year }}</td>
                                          <td>{{ sjr.value }}</td>
                                        </tr>
                                      </tbody>
                                  </v-simple-table>
                                </div>
                                <div
                                v-if="this.selected_publishing.journal.snip"
                                >
                                    <br>
                                    <h4>
                                        Tabela de SNIP
                                    </h4>
                                    <v-simple-table>
                                      <thead>
                                        <tr>
                                          <th class="text-left">Ano</th>
                                          <th class="text-left">SNIP</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr
                                        v-for="(snip, index) in this.selected_publishing.journal.snip"
                                        :key="index"
                                        >
                                          <td>{{ snip.year }}</td>
                                          <td>{{ snip.value }}</td>
                                        </tr>
                                      </tbody>
                                  </v-simple-table>
                                </div>
                                <br>
                                <div
                                v-if="this.selected_publishing.journal.links"
                                >
                                    <h4>
                                        Fonte do Scopus: {{this.selected_publishing.journal.links['scopus-source']}}
                                    </h4>
                                    <h4>
                                        Homepage: {{this.selected_publishing.journal.links['homepage']}}
                                    </h4>
                                </div>
                            </div>
                        </div>
                    </v-card-text>
                </v-card>
            </v-dialog>
            <!--
            <br>
            <h1>
                Gráficos
            </h1>

            <p>
                N de Publicações Recuperadas e Tempo Necessário para Recuperar as Publicações ( em ms )
            </p>
            <Charts
                v-if="display_graph"
                v-bind:data="records_collection"
                v-bind:my_options="records_options"
            />
            <br>
            <p>
                Tempo por Publicação Recuperada ( em ms )
            </p>
            <div
            class = "chart"
            >
                <Charts
                    v-if="display_graph"
                    v-bind:data="average_collection"
                    v-bind:my_options="average_options"
                />
            </div>
            -->
        </div>
    </div>
</template>

<script>
import citationsjson from '../citations.json';
import Charts from './Charts.vue';
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation';

export default {
    name : "Works",
    components : {
        Charts
    },
    computed: {
        /*
        filteredItems() {
            return this.jsondata.filter(item => {
                return item.sources[0].title.indexOf(this.search.toLowerCase()) > -1
            });
        }
        */
    },
    data () {
        return {
            no_orcid : false,
            loading : false,
            author_info : {},
            search : '',
            dialog : false,
            headers : [
                {
                    text : "Título",
                    align : "start",
                    sortable : true,
                    filterable : true,
                    value : "title"
                },
                {
                    text : "Ano",
                    sortable : true,
                    filterable : true,
                    value : "date"
                },
                {
                    text : "Local",
                    sortable : true,
                    filterable : true,
                    value : "source"
                },
                {
                    text : "Tipo",
                    value : "type"
                },
                {
                    text : "Nº of Sources",
                    value : "-"
                }
            ],
            selected_publishing : {},
            jsondata: [],
            
            /*
            author_info : {},
            display_graph : false,
            records_collection : {
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
            records_options : {},
            average_collection : {
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
            average_options : {}
            */
        }
    },
    async created () {
        this.loading = true;

        this.orcid_id = this.$route.params.id;
        
        var response = await fetch('http://localhost:5000/bo', {method : 'POST', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}, body: JSON.stringify({'orcid_id' : this.orcid_id})})

        console.log(response.status)

        if (response.status == 200) {

            var res = await response.json()

            console.log(res)
            
            // Author Info
            
            this.author_info = res['author_info']

            this.jsondata = res['publications']

            this.loading = false;
        
        }

        /*

            this.loading = false;

            // send info regarding the collecting of the current records

            var fetch_data = {
                'fetched_records' : this.jsondata.length,
                'fetch_time' : diff

            }

            fetch('http://localhost:5000/records', {method : 'POST', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}, body: JSON.stringify(fetch_data)})

            // get info regarding previous record collecting times

            var rec_res = await fetch('http://localhost:5000/records', {headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}})
            
            var rec_data = await rec_res.json()

            var avg_time = 0

            var total_avg_time = 0

            for (var it = 0 ; it < rec_data['records'].length ; it++) {
                var rec = rec_data['records'][it]
                this.records_collection.labels.push(rec['id'])
                this.average_collection.labels.push(rec['id'])
                
                this.records_collection.datasets[0].data.push(rec['fetched_records'])
                this.records_collection.datasets[1].data.push(rec['fetch_time'])
                this.average_collection.datasets[0].data.push(rec['fetch_time'] / rec['fetched_records'])

                total_avg_time += rec['fetch_time']
                avg_time += (rec['fetch_time'] / rec['fetched_records'])
                //console.log(rec)
            }

            total_avg_time /= this.records_collection.datasets[1].data.length
            avg_time /= this.average_collection.datasets[0].data.length

            var most_records = Math.max.apply(Math, this.records_collection.datasets[0].data)

            var longest_time = Math.max.apply(Math, this.records_collection.datasets[1].data)

            // feed graph settings

            this.records_options = {
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
            
            this.average_options = {
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
        */
        else {
            console.log('Not 200!')
            this.loading = false;
            this.no_orcid = true;
        }
    },
    methods: {
        async handleClick(str) {
            this.loading = true;
            console.log(str)
            this.selected_publishing = {}
            this.selected_publishing.title = str['title']
            this.selected_publishing.date = str['date']
            this.selected_publishing.type = str['type']
            this.selected_publishing.eid = str.eid;
            this.selected_publishing.wosuid = str.wosuid;
            this.selected_publishing.authors = [];
            this.selected_publishing.citedby = str['citation-count'];
            this.selected_publishing.publishing_link = str['journal']['scopus-source'];
            this.selected_publishing.issn = str['journal']['issn'];
            this.selected_publishing.journal = {}
            if (this.selected_publishing.eid != undefined) {
                for (var it = 0; it < str.authors.length ; it++) {
                    this.selected_publishing.authors.push({
                        "indexed_name" : str.authors[it]['indexed-name'],
                        "given_name" : str.authors[it]['name']
                    });
                }
                
                if (this.selected_publishing.issn) {
                    this.selected_publishing.journal.title = str['journal']['name']
                    this.selected_publishing.journal.publisher = str['journal']['publisher']
                    this.selected_publishing.journal.start_year = str['journal']['start_year']
                    this.selected_publishing.journal.end_year = str['journal']['end_year']
                    this.selected_publishing.journal.eissn = str['journal']['eissn']
                    this.selected_publishing.journal.source_id = str['journal']['id']

                    this.selected_publishing.journal.quartiles_href = "https://www.scimagojr.com/journalsearch.php?q=" + this.selected_publishing.journal.source_id + "&tip=sid&clean=0"
                    this.selected_publishing.journal.quartiles_src = "https://www.scimagojr.com/journal_img.php?id=" + this.selected_publishing.journal.source_id
                    
                    this.selected_publishing.journal.subject_areas = []
                    for (var it = 0 ; it < str['journal']['subject_areas'].length ; it++) this.selected_publishing.journal.subject_areas.push(str['journal']['subject_areas'][it])

                    this.selected_publishing.journal.snip = []
                    for (var it = 0 ; it < str['journal']['snip'].length ; it++ ) this.selected_publishing.journal.snip.push({ 'year' : str['journal']['snip'][it]['year'], 'value' : str['journal']['snip'][it]['value']})

                    this.selected_publishing.journal.sjr = []
                    for (var it = 0 ; it < str['journal']['sjr'].length ; it++ ) this.selected_publishing.journal.sjr.push({ 'year' : str['journal']['sjr'][it]['year'], 'value' : str['journal']['sjr'][it]['value']})
                    
                    this.selected_publishing.journal.links = new Map()
                    this.selected_publishing.journal.links['scopus-source'] = str['journal']['scopus_source']
                    this.selected_publishing.journal.links['homepage'] = str['journal']['homepage']
                    /*
                    <div
                    v-if="this.selected_publishing.journal.citescore"
                    >
                        <br>
                        <h4>
                            CiteScore
                        </h4>
                        <v-simple-table>
                              <thead>
                                <tr>
                                  <th class="text-left">Ano</th>
                                  <th class="text-left">CiteScore</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td> {{this.selected_publishing.journal.citescore.currentMetricYear}} </td>
                                  <td> {{this.selected_publishing.journal.citescore.currentMetric}} </td>
                                </tr>
                                <tr>
                                  <td> {{this.selected_publishing.journal.citescore.trackerYear}} </td>
                                  <td> {{this.selected_publishing.journal.citescore.tracker}} </td>
                                </tr>
                              </tbody>
                          </v-simple-table>
                        <br>
                    </div>
                    >
                    */
                    console.log(str['journal']['citescore'].length)
                    if (str['journal']['citescore'].length) {
                        console.log("positive length")
                        this.selected_publishing.journal.citescore = {}
                        this.selected_publishing.journal.citescore.currentMetric = str['journal']['citescore'][0]['value']
                        this.selected_publishing.journal.citescore.currentMetricYear = str['journal']['citescore'][0]['year']
                    }
                    else this.selected_publishing.journal.citescore = null
                    if (str['journal']['citescore'].length == 2) {
                        this.selected_publishing.journal.citescore.tracker = str['journal']['citescore'][1]['value']
                        this.selected_publishing.journal.citescore.trackerYear = str['journal']['citescore'][1]['value']
                        this.selected_publishing.journal.citescore.widgetLink = "https://www.scimagojr.com/journalsearch.php?q=" + this.selected_publishing.journal.source_id + "&tip=sid&clean=0"
                    }
                    else {
                        this.selected_publishing.journal.citescore.tracker = null
                        this.selected_publishing.journal.citescore.trackerYear = null
                    }
                }
                else this.selected_publishing.journal = null
            }
            else this.selected_publishing.wosuid = str.wosuid;
            this.dialog = true;
            this.loading = false;
        }
    },
    watch: {
        dialog(val) {
            if (val) console.log("Val is true!")
            else this.selected_publishing = {}
        }
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

.chart {
    width : '50%'
}

</style>

<!--
<template>
    <div>
        <div
        v-if = "no_orcid">
            <h1>
                Não existe nenhum utilizador com o ORCID: {{this.orcid_id}}
            </h1>
        </div>
        <div
        v-else
        >
            <h1>
            Informação sobre o/a Autor(a)
            </h1>
            <br>
            <v-card
            class = "card"
            >
                <v-card-title
                class = "center-card-text"
                >
                    {{this.author_info.given_name}} {{this.author_info.surname}}
                </v-card-title>
                <v-card-text>
                    <div
                    class = "center-card-text"
                    >
                        <h3>
                            Informações:
                        </h3>
                        <v-divider></v-divider>
                        <h4>
                            Orcid: {{this.author_info.orcid_id}}
                        </h4>
                        <h4>
                            Citações: {{this.author_info.citation_count}}
                        </h4>
                        <h4>
                            Citado por: {{this.author_info.cited_by_count}}
                        </h4>
                        <br>
                        <h3>
                            Áreas de Interesse:
                        </h3>
                        <v-divider></v-divider>
                        <br>
                        <div
                        class = "text-center"
                        >
                            <v-chip
                            class = "ma-2"
                            v-for="(subj, index) in this.author_info.subject_areas"
                            :key="index"
                            >
                                {{subj}}
                            </v-chip>
                        </div>
                    </div>
                </v-card-text>
            </v-card>
            <br>
            <h1>
                Publicações
            </h1>
            <br>
            <v-card
            class = "card"
            >
                <v-card-title>
                    <v-text-field
                    v-model="search"
                    append-icon="mdi-search"
                    label="Filtrar por Título"
                    single-line
                    hide-details
                    ></v-text-field>
                </v-card-title>
                <v-progress-circular
                class = "progress"
                v-if="loading"
                :size="70"
                :width="7"
                color="blue-grey darken-4"
                indeterminate
                ></v-progress-circular>
                <v-data-table
                loading-text = "A carregar publicações"
                no-data-text = "Não existem publicações associadas ao OrcID fornecido"
                :headers = "headers"
                :items = "jsondata"
                :items-per-page = 10
                :search = "search"
                @click:row="handleClick"
                >
                </v-data-table>
            </v-card>
            <br>
            <v-dialog
            v-model="dialog"
            width="800"
            height="500"
            v-if="this.dialog == true"
            >
                <v-card>
                    <v-card-title>
                        {{this.selected_publishing.title}}
                    </v-card-title>
                    <v-card-text>
                        <div
                        class = "center-card-text"
                        >
                            <br>
                            <h3>
                                Publicação foi citada {{this.selected_publishing.citedby}} vez(es)
                            </h3>
                            <br>
                            <h3>
                                Data: {{this.selected_publishing.publish_date}} | Tipo de Publicação: {{this.selected_publishing.type}}
                            </h3>
                            <v-divider></v-divider>
                            <h4
                            v-if="this.selected_publishing.wosuid != ''"
                            >
                            WOSUID : {{this.selected_publishing.wosuid}}
                            </h4>
                            <div
                            >
                                <h4
                                v-if="this.selected_publishing.publishing_link != ''"
                                >
                                    <a
                                    style = "text-decoration:none; color:#555" 
                                    v-bind:href=this.selected_publishing.publishing_link
                                    >
                                        EID : {{this.selected_publishing.eid}}
                                    </a>
                                </h4>
                                <br>
                                <h3>
                                    Autores:
                                </h3>
                                <v-divider></v-divider>
                                <h4
                                v-for="(author_name, index) in this.selected_publishing.authors"
                                :key="index"
                                >
                                    {{author_name.given_name}} {{author_name.surname}} - ({{author_name.indexed_name}})
                                </h4>
                            </div>
                            <br>
                            <div
                            v-if = "this.selected_publishing.journal != null"
                            >
                                <br>
                                <h3>
                                    Informações do Local de Publicação
                                </h3>
                                <v-divider></v-divider>
                                <h4>
                                    Nome: {{this.selected_publishing.journal.title}}
                                </h4>
                                <h4>
                                    Publicante: {{this.selected_publishing.journal.publisher}}
                                </h4>
                                <h4>
                                    ISSN: {{this.selected_publishing.journal.issn}}
                                </h4>
                                <h4
                                v-if="this.selected_publishing.journal.eissn"
                                >
                                    eISSN: {{this.selected_publishing.journal.eissn}}
                                </h4>
                                <h4>
                                    Início de Operação: {{this.selected_publishing.journal.start_year}}
                                </h4>
                                <h4
                                v-if="this.selected_publishing.journal.end_year != 2020 & this.selected_publishing.journal.end_year != null"
                                >
                                    Fim de Operação: {{this.selected_publishing.journal.end_year}}
                                </h4>
                                 <div
                                v-if="this.selected_publishing.journal.citescore"
                                >
                                    <br>
                                    <h4>
                                        CiteScore
                                    </h4>
                                    <v-simple-table>
                                          <thead>
                                            <tr>
                                              <th class="text-left">Ano</th>
                                              <th class="text-left">CiteScore</th>
                                            </tr>
                                          </thead>
                                          <tbody>
                                            <tr>
                                              <td> {{this.selected_publishing.journal.citescore.currentMetricYear}} </td>
                                              <td> {{this.selected_publishing.journal.citescore.currentMetric}} </td>
                                            </tr>
                                            <tr>
                                              <td> {{this.selected_publishing.journal.citescore.trackerYear}} </td>
                                              <td> {{this.selected_publishing.journal.citescore.tracker}} </td>
                                            </tr>
                                          </tbody>
                                      </v-simple-table>
                                    <br>
                                </div>
                                <div
                                    v-if="this.selected_publishing.journal.source_id"
                                    >
                                        <h4>
                                            Quartiles
                                        </h4>
                                        <a
                                            v-bind:href=this.selected_publishing.journal.quartiles_href
                                            title="SCImago Journal &amp; Country Rank"
                                        >
                                            <img
                                                border="0"
                                                v-bind:src=this.selected_publishing.journal.quartiles_src
                                                alt="SCImago Journal &amp; Country Rank"
                                            />
                                        </a>
                                    </div>
                                <div
                                v-if = "this.selected_publishing.journal.subject_areas.length"
                                >
                                    <h4>
                                        Temas:
                                    </h4>
                                    <v-chip
                                    class = "ma-2"
                                    v-for="(subj, index) in this.selected_publishing.journal.subject_areas"
                                    :key="index"
                                    >
                                        {{subj}}
                                    </v-chip>
                                </div>
                                <div
                                v-if="this.selected_publishing.journal.sjr"
                                >
                                    <br>
                                    <h4>
                                        Tabela de SJR
                                    </h4>
                                    <v-simple-table>
                                      <thead>
                                        <tr>
                                          <th class="text-left">Ano</th>
                                          <th class="text-left">SJR</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr
                                        v-for="(sjr, index) in this.selected_publishing.journal.sjr"
                                        :key="index"
                                        >
                                          <td>{{ sjr.year }}</td>
                                          <td>{{ sjr.value }}</td>
                                        </tr>
                                      </tbody>
                                  </v-simple-table>
                                </div>
                                <div
                                v-if="this.selected_publishing.journal.snip"
                                >
                                    <br>
                                    <h4>
                                        Tabela de SNIP
                                    </h4>
                                    <v-simple-table>
                                      <thead>
                                        <tr>
                                          <th class="text-left">Ano</th>
                                          <th class="text-left">SNIP</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr
                                        v-for="(snip, index) in this.selected_publishing.journal.snip"
                                        :key="index"
                                        >
                                          <td>{{ snip.year }}</td>
                                          <td>{{ snip.value }}</td>
                                        </tr>
                                      </tbody>
                                  </v-simple-table>
                                </div>
                                <br>
                                <div
                                v-if="this.selected_publishing.journal.links"
                                >
                                    <h4>
                                        Fonte do Scopus: {{this.selected_publishing.journal.links['scopus-source']}}
                                    </h4>
                                    <h4>
                                        Homepage: {{this.selected_publishing.journal.links['homepage']}}
                                    </h4>
                                </div>
                            </div>
                        </div>
                    </v-card-text>
                </v-card>
            </v-dialog>
            <br>
            <h1>
                Gráficos
            </h1>

            <p>
                N de Publicações Recuperadas e Tempo Necessário para Recuperar as Publicações ( em ms )
            </p>
            <Charts
                v-if="display_graph"
                v-bind:data="records_collection"
                v-bind:my_options="records_options"
            />
            <br>
            <p>
                Tempo por Publicação Recuperada ( em ms )
            </p>
            <div
            class = "chart"
            >
                <Charts
                    v-if="display_graph"
                    v-bind:data="average_collection"
                    v-bind:my_options="average_options"
                />
            </div>
        </div>
    </div>
</template>

<script>
import citationsjson from '../citations.json';
import Charts from './Charts.vue';
import ChartAnnotationsPlugin from 'chartjs-plugin-annotation';

export default {
    name : "Works",
    components : {
        Charts
    },
    computed: {
        filteredItems() {
            return this.jsondata.filter(item => {
                return item.sources[0].title.indexOf(this.search.toLowerCase()) > -1
            });
        }
    },
    data () {
        return {
            no_orcid : false,
            loading : false,
            orcid : '',
            search : '',
            dialog : false,
            page : 1,
            perPage : 50,
            headers : [
                {
                    text : "Título",
                    align : "start",
                    sortable : true,
                    filterable : true,
                    value : "sources[0].title"
                },
                {
                    text : "Ano",
                    sortable : true,
                    filterable : true,
                    value : "sources[0].publish_date"
                },
                {
                    text : "Local",
                    sortable : true,
                    filterable : true,
                    value : "sources[0].name"
                },
                {
                    text : "Tipo",
                    value : "sources[0].type"
                },
                {
                    text : "Nº of Sources",
                    value : "sources.length"
                }
            ],
            selected_publishing : {},
            jsondata: [],
            citation_count : "-",
            scopus_api_key : "43471229f9ff8ba1c9ec4faeb189b6f4",
            scopus_id : "38349047757",
            scopus_citations_p1 : "http://api.elsevier.com/content/abstract/scopus_id/",
            scopus_citations_p2 : "?field=authors,title,publicationName,volume,issueIdentifierprism:pageRange,coverDate,article-number,doi,issn,citedby-count,prism:aggregationType",
            scopus_abstract : "https://api.elsevier.com/content/abstract/citations?scopus_id=38349047757&apiKey=43471229f9ff8ba1c9ec4faeb189b6f4&httpAccept=application%2Fjson",
            scopus_title : "https://api.elsevier.com/content/serial/title/issn/1947-315X?apiKey=43471229f9ff8ba1c9ec4faeb189b6f4&httpAccept=application%2Fjson",
            issn : "1947-315X",
            quartiles : '<a href="https://www.scimagojr.com/journalsearch.php?q=130124&amp;tip=sid&amp;exact=no" title="SCImago Journal &amp; Country Rank"><img border="0" src="https://www.scimagojr.com/journal_img.php?id=130124" alt="SCImago Journal &amp; Country Rank"  /></a>',
            author_info : {},
            display_graph : false,
            records_collection : {
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
            records_options : {},
            average_collection : {
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
            average_options : {}
        }
    },
    async created () {
        
        this.loading = true;

        this.orcid_id = this.$route.params.id;

        var orcid_link = "https://pub.orcid.org/v2.0/" + this.orcid_id;

        var source_array = [];

        // get researcher publishings

        var beg_time = new Date().getTime();

        var response = await fetch(orcid_link + "/works/", {headers : {"Accept" : "application/json"}})

        console.log(response.status)

        if (response.status == 200) {

            var data = await response.json();

            var end_time = new Date().getTime();

            var diff = end_time - beg_time;

            console.log(diff);

            // processing publishings into appropriate data structures

            for (var i = 0; i < data.group.length ; i++) { // group
                var toAdd = {};
                toAdd.sources = [];
                for (var it = 0 ; it < data.group[i]["work-summary"].length ; it++) { // work_summary aka preferred sources
                    if (data.group[i]["work-summary"][it]["source"]["source-name"].value == 'Scopus - Elsevier' || data.group[i]["work-summary"][it]["source"]["source-name"].value == 'ResearcherID') {
                        var source = {};
                        // assigning the information related to the source in question
                        source.name = data.group[i]["work-summary"][it]["source"]["source-name"].value;
                        source.title = data.group[i]["work-summary"][it].title.title.value.charAt(0).toUpperCase() + data.group[i]["work-summary"][it].title.title.value.slice(1);
                        source.publish_date = new Date (data.group[i]["work-summary"][it]["created-date"].value).getFullYear();
                        source.authors = [];
                        source.type = data.group[i]["work-summary"][it].type.toLowerCase();
                        source.source_map = new Map();
                        source.doi = "-";
                        source.eid = "-";
                        source.wosuid = "-";
                        if (data.group[i]["work-summary"][it]["external-ids"]) {
                            for (var e_id = 0 ; e_id < data.group[i]["work-summary"][it]["external-ids"]["external-id"].length ; e_id++) { // external_ids
                                source.source_map.set(data.group[i]["work-summary"][it]["external-ids"]["external-id"][e_id]["external-id-type"], data.group[i]["work-summary"][it]["external-ids"]["external-id"][e_id]["external-id-value"]);
                                
                                switch (data.group[i]["work-summary"][it]["external-ids"]["external-id"][e_id]["external-id-type"]) {
                                    case "doi":
                                        // 2
                                        source.doi = data.group[i]["work-summary"][it]["external-ids"]["external-id"][e_id]["external-id-value"];
                                        break;
                                    case "eid":
                                        // 0 
                                        // if the source type has eid then we have to add the remaining authors / citation information
                                        source.eid = data.group[i]["work-summary"][it]["external-ids"]["external-id"][e_id]["external-id-value"];
                                        break;
                                    case "wosuid":
                                        // 1
                                        source.wosuid = data.group[i]["work-summary"][it]["external-ids"]["external-id"][e_id]["external-id-value"];
                                    default:
                                }
                                
                            }
                            if (source.name == 'Scopus - Elsevier') toAdd.sources.splice(0,0,source);
                            else toAdd.sources.splice(1,0,source);
                        }
                    }
                }
                if (toAdd.sources.length > 0) this.jsondata.push(toAdd);
            }

            // get author info

            var test_res = await fetch('http://localhost:5000/author_info', {method : 'POST', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}, body: JSON.stringify({'orcid' : this.orcid_id})})

            var test_json = await test_res.json()

            this.author_info.citation_count = test_json['coredata']['citation-count']
            this.author_info.cited_by_count = test_json['coredata']['cited-by-count']
            this.author_info.orcid_id = this.orcid_id
            this.author_info.given_name = test_json['preferred-name']['given-name']
            this.author_info.surname = test_json['preferred-name']['surname']
            this.author_info.subject_areas = []
            for (var it = 0 ; it < test_json['subject-areas']['subject-area'].length ; it++ ) this.author_info.subject_areas.push(test_json['subject-areas']['subject-area'][it]['$'])

            console.log(this.author_info)

            this.loading = false;

            // send info regarding the collecting of the current records

            var fetch_data = {
                'fetched_records' : this.jsondata.length,
                'fetch_time' : diff

            }

            fetch('http://localhost:5000/records', {method : 'POST', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}, body: JSON.stringify(fetch_data)})

            // get info regarding previous record collecting times

            var rec_res = await fetch('http://localhost:5000/records', {headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}})
            
            var rec_data = await rec_res.json()

            var avg_time = 0

            var total_avg_time = 0

            for (var it = 0 ; it < rec_data['records'].length ; it++) {
                var rec = rec_data['records'][it]
                this.records_collection.labels.push(rec['id'])
                this.average_collection.labels.push(rec['id'])
                
                this.records_collection.datasets[0].data.push(rec['fetched_records'])
                this.records_collection.datasets[1].data.push(rec['fetch_time'])
                this.average_collection.datasets[0].data.push(rec['fetch_time'] / rec['fetched_records'])

                total_avg_time += rec['fetch_time']
                avg_time += (rec['fetch_time'] / rec['fetched_records'])
                //console.log(rec)
            }

            total_avg_time /= this.records_collection.datasets[1].data.length
            avg_time /= this.average_collection.datasets[0].data.length

            var most_records = Math.max.apply(Math, this.records_collection.datasets[0].data)

            var longest_time = Math.max.apply(Math, this.records_collection.datasets[1].data)

            // feed graph settings

            this.records_options = {
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
            
            this.average_options = {
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
        else {
            this.loading = false;
            this.no_orcid = true;
        }

    },
    methods: {
        async handleClick(str) {
            this.loading = true;
            this.selected_publishing = str.sources[0];
            this.selected_publishing.eid = '';
            this.selected_publishing.wosuid = '';
            this.selected_publishing.authors = [];
            this.selected_publishing.citedby = 0;
            this.selected_publishing.publishing_link = '';
            this.selected_publishing.issn = '';
            if (this.selected_publishing.source_map.get("eid") != undefined) {
                this.selected_publishing.eid = this.selected_publishing.source_map.get("eid");
                this.selected_publishing.publishing_link = "http://www.scopus.com/record/display.url?eid=" + this.selected_publishing.eid + "&origin=resultslist"
                var url = "http://localhost:5000/publishings"

                var publ_info = {
                    'scopus_id' : this.selected_publishing.eid.substring(7)
                }

                let res = await fetch(url, {method : 'POST', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}, body: JSON.stringify(publ_info)})

                let res_data = await res.json()

                console.log(res_data)

                for (var it = 0; it < res_data["abstracts-retrieval-response"]["authors"]["author"].length ; it++) {
                    console.log("Author #" + (it + 1) + " is called -> " + res_data["abstracts-retrieval-response"]["authors"]["author"][it]["ce:indexed-name"]);
                    this.selected_publishing.authors.push({
                        "indexed_name" : res_data["abstracts-retrieval-response"]["authors"]["author"][it]["ce:indexed-name"],
                        "given_name" : res_data["abstracts-retrieval-response"]["authors"]["author"][it]["ce:given-name"],
                        "surname" : res_data["abstracts-retrieval-response"]["authors"]["author"][it]["ce:surname"],
                    });
                }
                
                this.selected_publishing.citedby = res_data["abstracts-retrieval-response"]["coredata"]["citedby-count"];
                
                console.log(res_data["abstracts-retrieval-response"]['coredata'])
                if (res_data["abstracts-retrieval-response"]['coredata']['prism:issn']) {
                    var issn = res_data["abstracts-retrieval-response"]['coredata']['prism:issn'].split(' ')
                    this.selected_publishing.journal = {}
                    this.selected_publishing.journal.issn = issn[0]
                    var issn_res = await fetch("http://localhost:8080/content/serial/title/issn/" + this.selected_publishing.journal.issn + "?apiKey=43471229f9ff8ba1c9ec4faeb189b6f4")
                    if (issn_res.status == 200) {
                        var issn_data = await issn_res.json();

                        if (issn_data['serial-metadata-response']['entry'].length) {
                            this.selected_publishing.journal.title = issn_data['serial-metadata-response']['entry'][0]['dc:title']
                            this.selected_publishing.journal.publisher = issn_data['serial-metadata-response']['entry'][0]['dc:publisher']
                            this.selected_publishing.journal.start_year = issn_data['serial-metadata-response']['entry'][0]['coverageStartYear']
                            this.selected_publishing.journal.end_year = issn_data['serial-metadata-response']['entry'][0]['coverageEndYear']
                            this.selected_publishing.journal.eissn = issn_data['serial-metadata-response']['entry'][0]['prism:eissn']
                            this.selected_publishing.journal.source_id = res_data["abstracts-retrieval-response"]["coredata"]["source-id"]
                            this.selected_publishing.journal.quartiles_href = "https://www.scimagojr.com/journalsearch.php?q=" + this.selected_publishing.journal.source_id + "&tip=sid&clean=0"
                            this.selected_publishing.journal.quartiles_src = "https://www.scimagojr.com/journal_img.php?id=" + this.selected_publishing.journal.source_id
                            console.log(this.selected_publishing.journal.quartiles_href, this.selected_publishing.journal.quartiles_src)
                            this.selected_publishing.journal.subject_areas = []
                            if (issn_data['serial-metadata-response']['entry'][0]['subject-area']) for (var it = 0 ; it < issn_data['serial-metadata-response']['entry'][0]['subject-area'].length ; it++) this.selected_publishing.journal.subject_areas.push(issn_data['serial-metadata-response']['entry'][0]['subject-area'][it]['$'])

                            this.selected_publishing.journal.snip = []
                            if (issn_data['serial-metadata-response']['entry'][0]['SNIPList']) for (var it = 0 ; it < issn_data['serial-metadata-response']['entry'][0]['SNIPList']['SNIP'].length ; it++ ) this.selected_publishing.journal.snip.push({ 'year' : issn_data['serial-metadata-response']['entry'][0]['SNIPList']['SNIP'][it]['@year'], 'value' : issn_data['serial-metadata-response']['entry'][0]['SNIPList']['SNIP'][it]['$']})

                            this.selected_publishing.journal.sjr = []
                            if (issn_data['serial-metadata-response']['entry'][0]['SJRList']) for (var it = 0 ; it < issn_data['serial-metadata-response']['entry'][0]['SJRList']['SJR'].length ; it++ ) this.selected_publishing.journal.sjr.push({ 'year' : issn_data['serial-metadata-response']['entry'][0]['SJRList']['SJR'][it]['@year'], 'value' : issn_data['serial-metadata-response']['entry'][0]['SJRList']['SJR'][it]['$']})
                            
                            this.selected_publishing.journal.links = new Map()
                            if (issn_data['serial-metadata-response']['entry'][0]['link']) for (var it = 0 ; it < issn_data['serial-metadata-response']['entry'][0]['link'].length ; it ++) this.selected_publishing.journal.links[issn_data['serial-metadata-response']['entry'][0]['link'][it]['@ref']] = issn_data['serial-metadata-response']['entry'][0]['link'][it]['@href']

                            if (issn_data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']) {
                                this.selected_publishing.journal.citescore = {}
                                this.selected_publishing.journal.citescore.currentMetric = issn_data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreCurrentMetric']
                                this.selected_publishing.journal.citescore.currentMetricYear = issn_data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreCurrentMetricYear']
                                this.selected_publishing.journal.citescore.tracker = issn_data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreTracker']
                                this.selected_publishing.journal.citescore.trackerYear = issn_data['serial-metadata-response']['entry'][0]['citeScoreYearInfoList']['citeScoreTrackerYear']   
                                this.selected_publishing.journal.citescore.widgetLink = this.selected_publishing.journal.links['scopus-source'].substr(0,23) + "sourceid/" + this.selected_publishing.journal.links['scopus-source'].substr(54, this.selected_publishing.journal.links['scopus-source'].length) + "?dgcid=sc_widget_citescore"
                            }
                            else this.selected_publishing.journal.citescore = null
                        }
                    }
                    else {
                        this.selected_publishing.journal = null
                        console.log("ISSN Not 200")
                        console.log(issn_res)
                    }
                }
            }
            else this.selected_publishing.wosuid = this.selected_publishing.source_map.get("wosuid");
            this.dialog = true;
            this.loading = false;
        }
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
-->