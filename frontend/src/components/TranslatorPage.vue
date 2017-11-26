<template>
  <div id='translatorpage'>
    <UserInfo></UserInfo>
    <Assignments></Assignments>
  </div>
</template>

<script>
  import UserInfo from '@/components/UserInfo'
  import Assignments from '@/components/Assignments'
  // TODO： add ADs

  export default {
    name: 'translatorpage',
    components: {
      UserInfo, Assignments
    },
    data () {
      return {
      }
    }
  }
</script>

<style scoped>

</style>
