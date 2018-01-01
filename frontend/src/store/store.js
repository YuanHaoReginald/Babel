import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    online: false
  },
  mutations: {
    'login': (state) => {
      state.online = true
    },
    'logout': (state) => {
      state.online = false
    }
  }
})
