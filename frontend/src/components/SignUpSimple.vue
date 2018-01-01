<template>
  <div class="root">
    <div class="container">
    <div class="title"><h2>加入巴别塔</h2></div>
      <br>
      <div class="input">
        <h3>用户名:</h3>
        <Input v-model="username" style="width: 400px"> </Input>
      </div>
      <br>
      <div class="input">
        <h3>密码:</h3>
        <Input v-model="password" type="password" style="width: 400px"> </Input>
      </div>
      <br>
      <div class="input">
        <h3>确认密码:</h3>
        <div>
          <Input v-model="passwordRepeat" type="password" style="width: 400px"> </Input>
          <Icon type="close-circled" v-if="passwordMatch === false" style="color: red"></Icon>
        </div>
      </div>
      <br>
      <div class="input">
        <h3>Email:</h3>
        <Input v-model="email" style="width: 400px"> </Input>
      </div>
      <br>
      <div class="button" @click="sign_up_simple">
        <Button size="large" type="primary" v-if="passwordMatch">Sign Up</Button>
        <Button size="large" type="primary" v-else disabled>Sign Up</Button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'sign_up_simple',
    data () {
      return {
        username: '',
        password: '',
        passwordRepeat: '',
        email: ''
      }
    },
    methods: {
      sign_up_simple: function () {
        let body = JSON.stringify({username: this.username,
          password: this.password,
          email: this.email,
          utype: this.$route.params.utype})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/UserSignUp', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data['id'] === 0) {
              that.$Message.warning('The username has already been picked, please retry.')
            } else {
              sessionStorage.setItem('userid', data.id)
              sessionStorage.setItem('utype', that.$route.params.utype)
              that.$router.push('/signupmore')
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      }
    },
    computed: {
      passwordMatch: function () {
        return this.password === this.passwordRepeat
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
  }
  .container {
    margin: 0 auto;
    width:400px;
  }
  .title {
    width:400px;
    margin-bottom: 20px;
  }
  .input {
    margin: 0;
  }
  h2 {
    color: #1c2438;
    text-align: left;
    font-size:40px;
  }
  h3 {
    color: #1c2438;
    text-align: left;
  }

</style>
