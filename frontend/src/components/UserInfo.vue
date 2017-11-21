<template>
  <div class="userinfo">
    <img src="../assets/logo.png" width='100px' height='100px'>
    <h2>{{ nickname }}</h2>
    <h3>{{ email }}</h3>
  </div>
</template>

<script>
  export default {
    name: 'userinfo',
    data () {
      return {
        nickname: 'UserInfoTest',
        email: 'abcdefg@163.com'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h2 {
  font-size:40px;
}
</style>
