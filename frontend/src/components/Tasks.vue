<template>
  <div class="tasks">
    <ul id="add_new_task">
      <Icon type="plus"></Icon>
      Add New
    </ul>
    <li v-for="task in tasks">
      {{ task }}
    </li>
  </div>
</template>

<script>
  export default {
    name: 'tasks',
    data () {
      return {
        tasks: ['ENG', 'ESP', 'ARB']
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.tasks {
  padding-top: 50px;
  font-size:20px;
}
</style>
