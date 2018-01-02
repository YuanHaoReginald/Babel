import Vuex from 'vuex'
import Vue from 'vue'
import VuexPersistence from 'vuex-persist'

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
  reducer: state => ({
    online: state.online,
    userid: state.userid,
    utype: state.utype,
    username: state.username
  }),
  filter: (mutation) => (
    mutation.type === 'setStatus' ||
    mutation.type === 'login' ||
    mutation.type === 'logout'
  )
})

export default new Vuex.Store({
  state: {
    online: false,
    userid: 0,
    utype: '',
    username: ''
  },
  mutations: {
    'setStatus': (state, userInfo) => {
      state.userid = userInfo['userid']
      state.utype = userInfo['utype']
      state.username = userInfo['username']
    },
    'login': (state, userInfo) => {
      state.online = true
      state.userid = userInfo['userid']
      state.utype = userInfo['utype']
      state.username = userInfo['username']
    },
    'logout': (state) => {
      state.online = false
      state.userid = 0
      state.utype = ''
      state.username = ''
    }
  },
  plugins: [vuexLocal.plugin]
})
