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
      spanLeft: 5,
      spanRight: 19
    }
  }
}
</script>

<style scoped>
.userinfo {
  float: left;
  width: 30%;
}
.tasks {
  margin-left: 30%;
  width: 70%;
}

</style>