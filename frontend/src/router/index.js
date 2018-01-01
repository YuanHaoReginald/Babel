import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Welcome from '@/components/Welcome'
import SignUpSimple from '@/components/SignUpSimple'
import SignUpMore from '@/components/SignUpMore'
import SignUpEmployer from '@/components/SignUpEmployer'
import EmployerPage from '@/components/EmployerPage'
import TranslatorPage from '@/components/TranslatorPage'
import AddTask from '@/components/AddTask'
import Task from '@/components/TaskPage'
import Assignment from '@/components/AssignmentPage'
import Square from '@/components/Square'

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
      path: '/signup/:utype',
      name: 'Signup',
      component: SignUpSimple
    },
    {
      path: '/signupmore',
      name: 'Signupmore',
      component: SignUpMore
    },
    {
      path: '/signupEmployer',
      name: 'SignupEmployer',
      component: SignUpEmployer
    },
    {
      path: '/employer',
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
    },
    {
      path: '/task/:tid',
      name: 'task',
      component: Task
    },
    {
      path: '/assignment/:aid',
      name: 'assignment',
      component: Assignment
    },
    {
      path: '/square',
      name: 'square',
      component: Square
    }
    // nginx:no 404 -> index.html(history)
  ]
})
