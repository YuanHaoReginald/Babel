<template>
  <div class="root">
    <div class="title"><h2>登录</h2></div>
    <div class="input">
      <h3>用户名:</h3>
      <Input v-model="username" style="width: 300px"> </Input>
    </div>
    <div class="input">
      <h3>密码:</h3>
      <Input v-model="password" type="password" style="width: 300px"> </Input>
    </div>
    <div class="button">
      <Button size="large" type="primary" v-on:click="login">Sign in</Button>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'login',
    data () {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      login: function () {
        let body = JSON.stringify({username: this.username, password: this.password})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/UserSignIn', { method: 'POST',
          headers,
          mode: 'cors',
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data['id'] === 0) {
              that.$Message.warning('Username or Password Error')
            } else {
              sessionStorage.setItem('userid', data['id'])
              sessionStorage.setItem('utype', data['utype'])
              that.$store.commit('login', {'userid': Number(data['id']), 'utype': data['utype'], 'username': that.username})
              that.$router.push({name: data['utype']})
            }
          }).catch(function (ex) {
            alert('Network Error')
          })
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin-top: 100px;
    margin-left: auto;
    margin-right: auto;
    width: 300px;
  }
  .input {
    margin-top: 30px;
  }
  h2 {
    color: #1c2438;
    font-size:30px;
  }
  h3 {
    color: #1c2438;
    float: left;
    margin-bottom: 10px;
  }
  Button {
    margin-top: 30px;

  }
</style>
