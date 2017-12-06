<template>
  <div class="root">
    <div id="left">
      <div class="card"><Card dis-hover>
      </Card></div>
    </div>
    <div id="right">
      <div class="card"><Card dis-hover>
        <h3 style="margin-bottom: 5px;">筛选任务</h3>
      </Card></div>
      <div class="card"><Card dis-hover>
      </Card></div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'square',
    data () {
      return {
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin:20px 127px 10px 127px;
    padding: 0 16px 0 16px;
    width:1000px;
  }
  #left {
    padding: 3px;
    float:left;
    width: 700px;
  }
  #right{
    padding: 3px;
    width: 300px;
    margin-left: 703px;
  }
  .card {
    margin-bottom: 10px;
  }
  #taskTitle {
    padding: 15px 20px 10px;
  }
  h2 {
    color: #1c2438;
    text-align: left;
  }
  h3 {
    font-size: 16px;
    color: #495060;
  }
  h4 {
    font-size: 14px;
    color: #495060;
    text-align: left;
  }
  p {
    font-size: 14px;
    color: #495060;
    text-align: left;
  }

</style>
