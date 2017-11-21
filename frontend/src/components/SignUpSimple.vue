<template>
  <div class="root">
    <Row>
      <Col span="16">
      <div class="title"><h2>Sign up for Babel</h2></div>
      <div class="input">
        <h3>Username:</h3>
        <Input v-model="username" style="width: 600px"> </Input>
      </div>
      <br>
      <div class="input">
        <h3>Password:</h3>
        <Input v-model="password" style="width: 600px"> </Input>
      </div>
      <br>
      <div class="button">
        <Button size="large" type="primary">Sign in</Button>
      </div>
      </Col>
      <Col span="8"></Col>
    </Row>
  </div>
</template>

<script>
  export default {
    name: 'sign_up_simple',
    data () {
      return {

      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin-top: 50px;
    margin-left: auto;
    margin-right: auto;
  }
  .title {
    margin: 20px;
  }
  .input {
    margin: 30px;
  }
  h2 {
    font-size:40px;
  }

</style>