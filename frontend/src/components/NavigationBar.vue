<template>
  <div id="root">
    <Menu mode="horizontal" :theme="theme1" active-name="1">
      <div id="center">
      <Row>
        <Col span="2"><router-link to="/square"><h2>Babel</h2></router-link></Col>
        <Col span="10" offset="1">
        <Input v-model="search" icon="search"> </Input>
        </Col>
        <Col span="3"offset="8" v-if="status">
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
        <Submenu name="3">
          <template slot="title">
            <Icon type="alert-circled"></Icon>
            离线状态
          </template>
          <router-link to="/login"><MenuItem>登入</MenuItem></router-link>
          <router-link to="/"><MenuItem>注册</MenuItem></router-link>
        </Submenu>
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
        search: '',
        status: true
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
          that.$router.push('/login')
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      toProfile: function () {
        this.$router.push({name: sessionStorage.getItem('utype')})
      }
    }
  }
</script>
<style>
  h2 {
    font-size:24px;
    color: floralwhite;
  }
  h3 {
    color: floralwhite;
  }
  #root {
    min-width: 1050px;
  }
  #center {
    width:950px;
    margin-right: auto;
    margin-left: auto;
  }
</style>
