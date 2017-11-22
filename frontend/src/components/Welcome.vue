<template>
  <div class="root">
    <div class="welcome">
      <h2>{{ msg }}</h2>
    </div>
    <br>
    <div class="buttons">
      <Button shape="circle" size="large" v-on:click="status=true">Register</Button>
      <router-link to="/login"><Button type="primary" shape="circle" size="large">Sign in</Button></router-link>
    </div>
    <br>
    <div v-if="status" class="new_buttons">
      <router-link to="/signup"><Button shape="circle" size="large" >I am a translator.</Button></router-link>
      <router-link to="/signup"><Button shape="circle" size="large" >I am an employer.</Button></router-link>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'login',
    data () {
      return {
        msg: 'Welcome to Babel.',
        status: false
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .welcome {
    margin-top: 200px;
  }
  .buttons {
    margin-top: 100px;
  }
  .buttons Button {
    margin: 0 30px 0 30px;
  }
  .new_buttons {
    margin-left: -120px;
  }
  h2 {
    font-size:40px;
  }
</style>
