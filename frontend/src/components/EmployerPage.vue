<template>
  <div id='employerpage'>
    <Row>
      <Col span="4"><UserInfo></UserInfo></Col>
      <Col span="8"><Tasks></Tasks></Col>
    </Row>
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

</style>
