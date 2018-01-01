<template>
  <div class="root">
    <div class="welcome">
      <h2>{{ msg }}</h2>
    </div>
    <br>
    <div class="buttons">
      <Button shape="circle" size="large" v-on:click="status=true">注册</Button>
      <router-link to="/login"><Button type="primary" shape="circle" size="large">登录</Button></router-link>
    </div>
    <br>
    <div v-if="status" class="new_buttons">
      <router-link to="/signup/translator"><Button shape="circle" size="large" >我是翻译</Button></router-link>
      <router-link to="/signup/employer"><Button shape="circle" size="large" >我要发布翻译任务</Button></router-link>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'login',
    data () {
      return {
        msg: '欢迎来到巴别塔',
        status: false
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .welcome {
    margin-top: 170px;
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
    font-size:35px;
    color: black;
  }
</style>
