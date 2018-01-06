import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/store'
import Login from '@/components/Login'
import Welcome from '@/components/Welcome'
import SignUpSimple from '@/components/SignUpSimple'
import SignUpMore from '@/components/SignUpMore'
import EmployerPage from '@/components/EmployerPage'
import TranslatorPage from '@/components/TranslatorPage'
import AddTask from '@/components/AddTask'
import Task from '@/components/TaskPage'
import Assignment from '@/components/AssignmentPage'
import Square from '@/components/Square'
import Manager from '@/components/Manager'

Vue.use(Router)

const router = new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'welcome',
      meta: {
        notRequireAuth: true
      },
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
      path: '/employer',
      name: 'employer',
      meta: {
        requireAuth: true,
        requireType: 'employer'
      },
      component: EmployerPage
    },
    {
      path: '/translator',
      name: 'translator',
      meta: {
        requireAuth: true,
        requireType: 'translator'
      },
      component: TranslatorPage
    },
    {
      path: '/addTask',
      name: 'addTask',
      meta: {
        requireAuth: true,
        requireType: 'employer'
      },
      component: AddTask
    },
    {
      path: '/task/:tid',
      name: 'task',
      meta: {
        requireAuth: true
      },
      component: Task
    },
    {
      path: '/assignment/:aid',
      name: 'assignment',
      meta: {
        requireAuth: true
      },
      component: Assignment
    },
    {
      path: '/square',
      name: 'square',
      component: Square
    },
    {
      path: '/square/:keyword',
      name: 'search',
      component: Square
    },
    {
      path: '/manager',
      name: 'admin',
      meta: {
        requireAuth: true,
        requireType: 'manager'
      },
      component: Manager
    }
    // nginx:no 404 -> index.html(history)
  ]
})

router.beforeEach((to, from, next) => {
  console.log('1')
  console.log(to)
  if (to.matched.some(r => r.meta.requireAuth)) {
    console.log('2')
    if (Number(store.state.userid) !== 0) {
      if (to.matched.some(r => r.meta.requireType)) {
        console.log(to.meta.requireType)
        console.log(store.state.utype)
        if (to.meta.requireType !== store.state.utype) {
          // if (store.state.utype === 'translator') {
          //   next({
          //     path: '/translator'
          //   })
          // } else {
          //   next({
          //     path: '/employer'
          //   })
          // }
          next({
            path: '/' + store.state.utype
          })
        } else {
          next()
        }
      } else {
        next()
      }
    } else {
      next({
        path: '/login'
      })
    }
  } else if (to.matched.some(r => r.meta.notRequireAuth)) {
    console.log('3')
    if (Number(store.state.userid) !== 0) {
      console.log('5')
      next({
        path: '/square'
      })
    } else {
      console.log('6')
      next()
    }
  } else {
    console.log('4')
    next()
  }
})

export default router
