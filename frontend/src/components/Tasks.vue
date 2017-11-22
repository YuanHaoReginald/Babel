<template>
  <div class="root">
    <div id="add" class="card">
      <Card shadow class="add" padding=10>
        <div id="addIcon"><Icon type="plus-circled" size=35></Icon></div>
        <div id="addText"><h2>Add a new task</h2></div>
      </Card>
    </div>
    <div id="tasks" class="card">
      <Card shadow class="tasks"></Card>
    </div>
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
  .root {
    margin-left: 460px;
    width: 600px;
    padding: 20px;
  }
  .card {
    margin-bottom: 20px;
  }
  #addIcon {
    float: left;
  }
  #addText {
    text-align: left;
    margin-left: 60px;
  }
  h2 {
    color: #1c2438;
  }
</style>
