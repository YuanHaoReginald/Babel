<template>
  <div id='employerpage'>
    <UserInfo></UserInfo>
    <Tasks></Tasks>
  </div>
</template>

<script>
import UserInfo from '@/components/UserInfo'
import Tasks from '@/components/Tasks'

export default {
  name: 'employerpage',
  components: {
    UserInfo, Tasks
  },
  data () {
    return {
    }
  }
}
</script>

<style scoped>
  #employerpage {
    margin-left: auto;
    margin-right: auto;
  }
</style>
