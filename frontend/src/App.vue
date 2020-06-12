<template>
  <v-app>
    <Header />
    <router-view
    class = "router"
    ></router-view>
  </v-app>
</template>

<script>
import Header from './components/Header';

export default {
  name: 'App',

  components: {
    Header,
  },

  data: () => ({
    //
  }),
};
</script>

<style>

.router { 
  height : 100%;
  width : 85%;
  margin : auto;
  padding : 25px 0px;
}

</style>