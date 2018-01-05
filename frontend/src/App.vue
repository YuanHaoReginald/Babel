<template>
  <div id="app">
    <NavigationBar></NavigationBar>
    <router-view :key="key"></router-view>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar'
export default {
  name: 'app',
  components: {
    NavigationBar
  },
  computed: {
    key () {
      return this.$route.name !== undefined ? this.$route.name + new Date() : this.$route + new Date()
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}
</style>
