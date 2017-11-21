import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Welcome from '@/components/Welcome'
import SignUpSimple from '@/components/SignUpSimple'

Vue.use(Router);

export default new Router({
  //mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: Welcome
    },
      {
      path: '/login',
      name: 'Login',
      component: Login
    },//http://localhost:8080/#/login/
    {
      path: '/signup',
      name: 'Signup',
      component: SignUpSimple
    },
    //nginx:no 404 -> index.html(history)
  ]
})
