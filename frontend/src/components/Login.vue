<template>
  <div class="root">
    <div class="title"><h2>Login</h2></div>
    <div class="input">
      <h3>Username:</h3>
      <Input v-model="username" style="width: 300px"> </Input>
    </div>
    <div class="input">
      <h3>Password:</h3>
      <Input v-model="password" style="width: 300px"> </Input>
    </div>
    <div class="button">
      <Button size="large" type="primary">Sign in</Button>
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
