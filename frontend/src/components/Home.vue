<template>
    <div>
        <v-content>
            <v-container
                class="fill-height"
                fluid
            >
                <v-row
                align="center"
                justify="center"
                >
                    <v-card
                    shaped
                    elevation
                    class="elevation-12 card"
                    >
                        <h1>
                            Repositório Centralizado OrcID
                        </h1>
                        <v-card-subtitle>
                            <p>
                                OrcID Prof. Machado -> 0000-0003-4121-6169
                            </p>
                            <p>
                                OrcID Prof. Cristiana -> 0000-0001-8736-7443
                            </p>
                            <p>
                                OrcID Prof. Abelha -> 0000-0001-6457-0756
                            </p>
                            <p>
                                OrcID Prof. Hugo -> 0000-0003-3957-2121
                            </p>
                        </v-card-subtitle>
                        <v-card-text>
                            <v-form>
                                <v-text-field
                                    v-model="orcid_id"
                                    outlined
                                    label="Inserir OrcID a pesquisar"
                                    name="orcid"
                                    type="text"
                                    class = "pt-12"
                                />
                            </v-form>
                        </v-card-text>
                        <v-card-actions
                        class = "actions"
                        >
                            <router-link
                            v-bind:to="'/works/' + this.orcid_id"
                            >
                                <v-btn
                                class = "btn"
                                >
                                    Pesquisar
                                </v-btn>
                            </router-link>
                        </v-card-actions>
                        <v-card-text>
                            <v-form>
                                <v-text-field
                                    v-model="orcid_backoffice"
                                    outlined
                                    label="Inserir OrcID a adicionar ao backoffice"
                                    name="orcid"
                                    type="text"
                                    class = "pt-12"
                                />
                            </v-form>
                        </v-card-text>
                        <v-card-actions
                        class = "actions"
                        >
                            <v-btn
                            class = "btn"
                            v-on:click = "orcidToBackoffice"
                            >
                                Adicionar ao Backoffice
                            </v-btn>
                        </v-card-actions>
                        <br>
                    </v-card>
                </v-row>
                <v-row
                align="center"
                justify="center"
                >
                    <v-card
                    shaped
                    elevation
                    class="elevation-12 mt-5 card"
                    >
                        <v-card-title
                        style = "text-align : center;"
                        >
                            <h3>
                                ORCID IDs em Backoffice e o seu estado
                            </h3>
                        </v-card-title>
                        <v-data-table
                        hide-default-footer
                        @click:row="searchOrcid"
                        :headers = "headers"
                        :items = "backoffice_orcids"
                        :item-key = "orcid_id"
                        >
                      </v-data-table>
                      <v-divider></v-divider>
                      <br>
                    </v-card>
                </v-row>
            </v-container>
        </v-content>
    </div>
</template>

<script>
export default {
    name : "Home",
    data () {
        return {
            orcid_id : '',
            orcid_backoffice : '',
            headers : [
                {
                    text: 'ORCID ID',
                    value : 'orcid_id',
                    sortable : true
                },
                {
                    text : 'Name',
                    value : 'name'
                },
                {
                    text : 'Status',
                    value : 'status',
                    sortable : true
                },
                {
                    text : 'Last Update',
                    value : 'last_update'
                }
            ],
            backoffice_orcids : []
        }
    },
    async created() {
        console.log("created")
        var response = await fetch('http://localhost:5000/bo', {method : 'GET', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}})

            if (response.status == 200) {
                //console.log('200!')
                var res = await response.json()
                //console.log(res)
                this.backoffice_orcids = res['records']

            }
            
            else console.log('Not 200!')
    },
    methods: {
        searchOrcid(e) {
            this.$router.push({name: 'BackOfficeWorks', params: {id : e.orcid_id}})
        },
        async orcidToBackoffice(e) {
            console.log(this.orcid_backoffice)
         
            var response = await fetch('http://localhost:5000/bo', {method : 'PUT', mode : 'cors', headers : {'Content-Type' : 'application/json', 'Access-Control-Allow-Origin' : '*'}, body: JSON.stringify({'orcid_id' : this.orcid_backoffice})})

            if (response.status == 200) {
         
                console.log('200!')
         
            }
            
            else console.log('Not 200!')
        }
    }
}
</script>

<style>

.card {
    width : 75%;
    margin : auto;
    justify-content : center;
    text-align : center;
}

h1 {
    text-align : center;
    padding-top : 15px;
}

.actions {
    justify-content : center;
}

</style>