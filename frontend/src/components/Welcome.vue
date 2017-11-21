<template>
  <div class="welcome">
    <h2>{{ msg }}</h2>
  </div>
</template>

<script>
  export default {
    name: 'welcome',
    data () {
      return {
        msg: 'Welcome to Babel.'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.welcome {
  margin-top: 200px;
}
h2 {
  font-size:40px;
}
</style>
