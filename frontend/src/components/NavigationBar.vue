<template>
  <Menu mode="horizontal" :theme="theme1" active-name="1">
    <Row>
      <Col span="2"><h2>Babel</h2></Col>
      <Col span="10" offset="1">
        <Input v-model="search"  icon="search"> </Input>
      </Col>
      <Col span="3"offset="8" v-if="status">
        <Submenu name="3">
        <template slot="title">
          <Icon type="stats-bars"></Icon>
          个人中心
        </template>
        <MenuItem>个人主页</MenuItem>
        <MenuItem>修改个人信息</MenuItem>
        <MenuItem>登出</MenuItem>
      </Submenu>
      </Col>
      <Col span="3"offset="8" v-else="status">
      <router-link to="/login"><MenuItem><h3>Login</h3></MenuItem></router-link>
      </Col>
    </Row>
  </Menu>
</template>
<script>
  export default {
    data () {
      return {
        theme1: 'dark',
        serach: '',
        status: false
      }
    }
  }
</script>
<style>
  h2 {
    font-size:24px;
    color: floralwhite;
  }
  h3 {
    color: floralwhite;
  }
</style>
