<template>
  <div class="root">
    <Card shadow>
      <h2>hahahhaha</h2>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'userinfo',
    data () {
      return {
        username: 'm_username',
        email: 'abcdefg@163.com'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  Card {
    margin: 30px;
    width: auto;
  }
  h2 {
    color: black;
  }
</style>
