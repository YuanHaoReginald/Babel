<template>
  <div class="root">
    <Card shadow>
      <div>
        <img v-bind:src="headSrc" class="head">
        <h2>{{ username }}</h2>
      </div>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'userinfo',
    data () {
      return {
        username: '王小明',
        email: 'abcdefg@163.com',
        headSrc: '/src/assets/head_sample.jpg'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    float: left;
    width: 300px;
    padding: 20px;
    margin-left: 180px;
  }
  .head {
    width: 40%;
    margin: 10%;
  }
  h2 {
    color: black;
  }
</style>
