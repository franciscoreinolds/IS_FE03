import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import Works from '../components/Works.vue'
import BackOfficeWorks from '../components/BackOfficeWorks.vue'
import Graphs from '../components/Graphs.vue'
import Charts from '../components/Charts.vue'
Vue.use(VueRouter)

  const routes = [
    {
      path : '/',
      name : 'Home',
      component : Home
    },
    {
      path : '/works/:id',
      name : 'Works',
      component : Works
    },
    {
      path : '/charts',
      name : 'Charts',
      component : Charts
    },
    {
      path : '/bo_works/:id',
      name : 'BackOfficeWorks',
      component : BackOfficeWorks
    },
    {
      path : '/graphs',
      name : 'Graphs',
      component : Graphs
    }
  ]

const router = new VueRouter({
  routes
})

export default router
