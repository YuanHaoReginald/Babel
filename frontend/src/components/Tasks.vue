<template>
  <div class="root">
    <div id="add" class="card">
      <Card class="add" padding=10>
        <router-link to="/addtask"><div id="addIcon"><Icon type="android-add-circle" size=35></Icon></div></router-link>
        <div id="addText"><h2>创建新任务</h2></div>
      </Card>
    </div>
    <div id="tasks" class="card">
      <Card shadow class="tasks" padding=0>
        <div id="taskListTitle"><h2>我的任务</h2></div>
        <div>
          <ul>
            <li v-for="task in tasklist">
              <Card padding=10 @click.native="checkTaskDetail(task.id)">
                <p slot="title" id="taskTitle">
                  {{ task.title }}&nbsp;&nbsp;&nbsp;<span v-for="tag in task.tags"><Tag><h4>{{ tag }}</h4></Tag></span>
                </p>
                <p id="taskTime">起始时间：{{ task.publishTime }}&nbsp;&nbsp;&nbsp;截止时间：{{ task.ddlTime }}</p>
                <p id="taskDescription">{{ task.description }}</p>
              </Card>
            </li>
          </ul>
        </div>
      </Card>
      <div id="pages">
        <Page :total="page_total_num"></Page>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-new */
  export default {
    name: 'tasks',
    data () {
      return {
        tasklist: [
          {
            title: '中法信件翻译任务',
            publishTime: '2017-3-1',
            ddlTime: '2017-5-10',
            tags: ['art', 'math'],
            language: 'French',
            description: 'I am the description.I am the description.I am the description.' +
            'I am the description.I am the description.I am the description.I am the description.'
          },
          {
            title: 'title',
            publishTime: 'publishTime',
            ddlTime: 'ddlTime',
            tags: ['art', 'math'],
            language: 'English',
            description: 'I am the description.I am the description.I am the description.' +
            'I am the description.I am the description.I am the description.I am the description.'
          }
        ],
        page_total_num: 500,
        page_current_num: 1
      }
    },
    mounted: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetEmployerTasks', { method: 'GET',
        headers,
        credentials: 'include'})
      .then(function (response) {
        return response.json().then(function (data) {
          that.tasklist = []
          for (let task of data.taskList) {
            that.tasklist.push({
              id: task.id,
              title: task.title,
              publishTime: Date(task.publishTime),
              ddlTime: Date(task.ddlTime),
              tags: task.tag,
              language: task.language,
              description: task.description
            })
          }
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
    },
    methods: {
      checkTaskDetail: function (taskid) {
        this.$router.push('/task/' + taskid)
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
  #taskListTitle {
    text-align: left;
    padding: 10px 0 10px 20px;
  }
  #taskTitle {
    font-size: 16px;
    text-align: left;
  }
  #taskDescription {
    text-align: left;
    color: #495060;
  }
  #taskTime {
    font-size: 12px;
    text-align: left;
    color: #80848f;
  }
  #pages {
    padding: 20px;
  }
  h2 {
    font-size: 24px;
    color: #1c2438;
  }
  h4 {
    font-size: 12px;
  }
</style>
