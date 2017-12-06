<template>
  <div class="root">
    <div id="tasks" class="card">
      <Card shadow class="tasks" padding=0>
        <div id="taskListTitle"><h2>我的任务</h2></div>
        <div id="bigCheckBox">
          <Row>
            <Col span="3"><div id="checkText"><h4>筛选：</h4></div></Col>
            <Col span="15">
              <div id="checkBox">
                <CheckboxGroup v-model="filter">
                  <Checkbox label="艺术"></Checkbox>
                  <Checkbox label="历史"></Checkbox>
                  <Checkbox label="文学"></Checkbox>
                </CheckboxGroup>
              </div>
            </Col>
            <Col span="5">
              <Select v-model="sort" placeholder="<排序方式>">
                <Option v-for="item in sortList" :value="item.value" :key="item.value">{{ item.label }}</Option>
              </Select>
            </Col>
          </Row>
        </div>
        <div>
          <ul>
            <li v-for="task in tasklist">
              <Card padding=10>
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
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-new */
  export default {
    name: 'tasks',
    data () {
      return {
        filter: [],
        sort: '',
        sortList: [
          {
            label: '按发布时间',
            value: 'publishTime'
          },
          {
            label: '按最后动态时间',
            value: 'changeTime'
          }
        ],
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
            tags: ['art', 'history'],
            language: 'English',
            description: 'I am the description.I am the description.I am the description.' +
            'I am the description.I am the description.I am the description.I am the description.'
          }
        ]
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
  #checkText {
    margin-top: 3px;
  }
  #checkBox {
    float: left;
    margin-bottom: 15px;
  }
  #bigCheckBox {
    height: 20px;
    margin-top: 10px;
    margin-bottom: 20px;
  }
  #taskListTitle {
    text-align: left;
    padding: 20px 0 10px 20px;
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
  h2 {
    font-size: 20px;
    color: #1c2438;
  }
  h4 {
    font-size: 12px;
  }
</style>
