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

const router = new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: Welcome
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup/:utype',
      name: 'signup',
      component: SignUpSimple
    },
    {
      path: '/signupmore',
      name: 'signupmore',
      meta: {
        requireAuth: true
      },
      component: SignUpMore
    },
    {
      path: '/signupEmployer',
      name: 'signupEmployer',
      meta: {
        requireAuth: true
      },
      component: SignUpEmployer
    },
    {
      path: '/employer',
      name: 'employer',
      meta: {
        requireAuth: true
      },
      component: EmployerPage
    },
    {
      path: '/translator',
      name: 'translator',
      meta: {
        requireAuth: true
      },
      component: TranslatorPage
    },
    {
      path: '/addTask',
      name: 'addTask',
      meta: {
        requireAuth: true
      },
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

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => r.meta.requireAuth)) {
    if (sessionStorage.getItem('userid')) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()
  }
})

export default router
