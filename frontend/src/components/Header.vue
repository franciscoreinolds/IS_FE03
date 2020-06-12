<template>
    <div>
        <v-app-bar
        class = "navbar"
        dense
        dark
        height = 70px
        max-height = 70px
        >
        <router-link
        :to = "{path : '/'}"
        class = "router-link"
        >
            <v-toolbar-title
            class = "toolbar-title"
            >       
                IS FE03
            </v-toolbar-title>  
        </router-link> 
        </v-app-bar>
    </div>
</template>

<script>
export default {
    name : "Header",
    data: () => ({
        links : [
        ]
    })
}
</script>

<style scoped>

.text-field {
  height : 60px;
  width : 50px
}

.router-link {
    text-decoration : none;
}

.toolbar-title {
    color : #ffffff;
}

</style>