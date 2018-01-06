<template>
  <div id="root">
    <Menu mode="horizontal" :theme="theme1" active-name="1">
      <div id="center">
      <Row>
        <Col span="2" @click.native="toWebmain"><h2>Babel</h2></Col>
        <Col span="10" offset="1">
        <Input v-model="search" icon="search" @click.native="searchTask"> </Input>
        </Col>
        <Col span="3"offset="8" v-if="this.$store.state.online">
        <Submenu name="3">
          <template slot="title">
            <Icon type="stats-bars"></Icon>
          个人中心
          </template>
          <MenuItem @click.native="toProfile">个人主页</MenuItem>
          <router-link to="/signupmore"><MenuItem>修改个人信息</MenuItem></router-link>
          <MenuItem @click.native="logout">登出</MenuItem>
        </Submenu>
        </Col>
        <Col span="3"offset="8" v-else>
        <div class="icon">
          <Submenu name="3">
            <template slot="title">
              <Icon type="person" size="40"></Icon>
              游客
            </template>
            <router-link to="/login"><MenuItem>登入</MenuItem></router-link>
            <router-link to="/"><MenuItem>注册</MenuItem></router-link>
          </Submenu>
        </div>
        </Col>
      </Row>
      </div>
    </Menu>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        theme1: 'dark',
        search: ''
      }
    },
    methods: {
      logout: function () {
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/UserLogout', { method: 'POST',
          headers,
          credentials: 'include'})
        .then(function (response) {
          sessionStorage.removeItem('userid')
          sessionStorage.removeItem('utype')
          that.$Message.success('Logout successfully.')
          that.$store.commit('logout')
          that.$router.push('/login')
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      toProfile: function () {
        this.$router.push({name: this.$store.state.utype})
      },
      toWebmain: function () {
        if (this.$store.state.online) {
          this.$router.push({path: '/square'})
        } else {
          this.$router.push({path: '/'})
        }
      },
      searchTask: function () {
        if (this.search.trim() !== '') {
          this.$router.push({name: 'search', params: {keyword: this.search.trim()}})
        }
      }
    }
  }
</script>
<style>
  h2 {
    font-size:24px;
    color: floralwhite;
  }
  h2:hover {
    cursor: pointer;
  }
  h3 {
    color: floralwhite;
  }
  #root {
  }
  #center {
    margin-right: auto;
    margin-left: auto;
  }
  .icon {
    margin-top: 5px;
  }
</style>
