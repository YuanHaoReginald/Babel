import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    online: false,
    userid: 0,
    utype: ''
  },
  mutations: {
    'setStatus': (state, userInfo) => {
      state.userid = userInfo['userid']
      state.utype = userInfo['utype']
    },
    'login': (state, userInfo) => {
      state.online = true
      state.userid = userInfo['userid']
      state.utype = userInfo['utype']
    },
    'logout': (state) => {
      state.online = false
      state.userid = 0
      state.utype = ''
    }
  }
})
