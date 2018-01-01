import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

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
  }
})
