import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Welcome from '@/components/Welcome'
import SignUpSimple from '@/components/SignUpSimple'
import SignUpMore from '@/components/SignUpMore'
import EmployerPage from '@/components/EmployerPage'
import TranslatorPage from '@/components/TranslatorPage'
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
      path: '/signupmore',
      name: 'Signupmore',
      component: SignUpMore
    },
    {
      path: '/employer/:id',
      name: 'employer',
      component: EmployerPage
    },
    {
      path: '/translator',
      name: 'translator',
      component: TranslatorPage
    },
    {
      path: '/addTask',
      name: 'addTask',
      component: AddTask
    }
    // nginx:no 404 -> index.html(history)
  ]
})
