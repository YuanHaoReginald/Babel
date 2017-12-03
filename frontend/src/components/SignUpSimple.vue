<template>
  <div class="root">
    <div class="container">
    <div class="title"><h2>Join Babel</h2></div>
      <br>
      <div class="input">
        <h3>Username:</h3>
        <Input v-model="username" style="width: 400px"> </Input>
      </div>
      <br>
      <div class="input">
        <h3>Password:</h3>
        <Input v-model="password" style="width: 400px"> </Input>
      </div>
      <br>
      <div class="input">
        <h3>Email:</h3>
        <Input v-model="email" style="width: 400px"> </Input>
      </div>
      <br>
      <div class="button">
        <Button size="large" type="primary" v-on:click="sign_up_simple">Sign Up</Button>
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
              alert('Invalid username or password, please retry.')
            } else {
              sessionStorage.setItem("userid", data['id']);
              that.$router.push('/signupmore')
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
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
