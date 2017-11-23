import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Welcome from '@/components/Welcome'
import SignUpSimple from '@/components/SignUpSimple'
import EmployerPage from '@/components/EmployerPage'
import AddTask from '@/components/AddTask'

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
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/signup',
      name: 'Signup',
      component: SignUpSimple
    },
    {
      path: '/employer/:id',
      name: 'employer',
      component: EmployerPage
    },
    {
      path: '/addTask',
      name: 'addTask',
      component: AddTask
    }
    // nginx:no 404 -> index.html(history)
  ]
})
