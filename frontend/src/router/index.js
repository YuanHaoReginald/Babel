import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Welcome from '@/components/Welcome'
import EmployerPage from '@/components/EmployerPage'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: Welcome
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/employer/:id',
      name: 'EmployerPage',
      component: EmployerPage
    }

    // nginx:no 404 -> index.html(history)
  ]
})
