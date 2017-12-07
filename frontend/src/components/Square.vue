<template>
  <div class="root">
    <div id="left">
      <div class="card" v-for="task in tasklist" @click="checkTaskDetail(task.id)"><Card dis-hover>
        <div class="task" >
          <h4>标签：{{ toStr(task.tags) }}</h4>
          <h2>{{ task.title }}</h2>
          <ul>
            <li v-for="a in task.assignments">
              <span class="order">{{ a.order }}</span>
              <span class="words"><b>报酬</b>：{{ a.price }}</span>
              <span class="words"><b>状态</b>： {{ a.status }}</span>
              <span v-if="a.status == '已完成'"><b>任务评分</b>:&nbsp;<Rate disabled v-model="a.score"></Rate></span>
              <span v-if="a.status == '未领取'"><Button type="primary" size="small" @click="pickup(task.id, a.id)">领取任务</Button></span>
              <p class="description"><b>详情</b>： {{ a.description }}</p>
            </li>
          </ul>
        </div>
      </Card></div>
    </div>
    <div id="right">
      <div class="card" id="chosen"><Card dis-hover>
        <h3 style="margin-bottom: 5px;">筛选任务</h3>
        <div class="chosen_by">按标签</div>
        <CheckboxGroup v-model="chosen_tags">
          <Checkbox label="全选"></Checkbox>
          <Checkbox label="香蕉"></Checkbox>
          <Checkbox label="苹果"></Checkbox>
          <Checkbox label="西瓜"></Checkbox>
        </CheckboxGroup>
        <div class="chosen_by">按语言</div>
        <CheckboxGroup v-model="chosen_languages">
          <Checkbox label="全选"></Checkbox>
          <Checkbox label="英语"></Checkbox>
          <Checkbox label="法语"></Checkbox>
          <Checkbox label="德语"></Checkbox>
          <Checkbox label="俄语"></Checkbox>
          <Checkbox label="日语"></Checkbox>
          <Checkbox label="西班牙语"></Checkbox>
        </CheckboxGroup>
        <div class="chosen_by">按价格</div>
        <CheckboxGroup v-model="chosen_price">
          <Checkbox label="全选"></Checkbox>
          <Checkbox label="0-30元"></Checkbox>
          <Checkbox label="30-100元"></Checkbox>
          <Checkbox label="100元以上"></Checkbox>
        </CheckboxGroup>
      </Card></div>
      <div class="card"><Card dis-hover>
        <h3>ADs</h3>
        <div id="ads">此广告位常年招租</div>
      </Card></div>
    </div>
  </div>
</template>

<script>
  import { Checkbox } from 'iview'
  export default {
    components: {Checkbox},
    name: 'square',
    methods: {
      pickup: function (task, assignment) {
        let body = JSON.stringify({userid: sessionStorage.getItem('userid'),
          task_id: task,
          assignment_order: assignment})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        fetch('api/PickupAssignment', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            console.log('Success')
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      toStr: function (tags) {
        let str = ''
        for (let i = 0; i < tags.length; i++) {
          str = str + ' ' + tags[i]
        }
        return str
      },
      checkTaskDetail: function (taskid) {
        this.$router.push('/task/' + taskid)
      }
    },
    data () {
      return {
        theme: 'light',
        chosen_tags: [],
        chosen_languages: [],
        chosen_price: [],
        tasklist: [
          {
            id: 1,
            title: '中法信件翻译任务',
            publishTime: '2017-3-1',
            ddlTime: '2017-5-10',
            tags: ['art', 'math'],
            language: 'French',
            assignments: [
              {
                order: 1,
                description: '这个任务需要翻译我给出的pdf文档的第20-40页，注意主要人名的翻' +
                '译要与附录中的统一。完成情况好的话我一定会好评的。',
                status: '已完成',
                translator: '2333',
                score: 4,
                price: '20元'
              },
              {
                order: 2,
                description: 'PartII PartII PartII PartII PartII PartII ',
                status: '进行中',
                translator: '2333',
                score: 4,
                price: '20元'
              },
              {
                order: 3,
                description: 'PartIII PartIII PartIII PartIII PartIII PartIII ',
                status: '未领取',
                translator: '2333',
                score: 4,
                price: '20元'
              }
            ]
          },
          {
            id: 2,
            title: 'title',
            publishTime: 'publishTime',
            ddlTime: 'ddlTime',
            tags: ['art', 'math'],
            language: 'English',
            assignments: [
              {
                order: 1,
                description: '这个任务需要翻译我给出的pdf文档的第20-40页，注意主要人名的翻' +
                '译要与附录中的统一。完成情况好的话我一定会好评的。',
                status: '已完成',
                translator: '2333',
                score: 4,
                price: '20元'
              },
              {
                order: 2,
                description: 'PartII PartII PartII PartII PartII PartII ',
                status: '进行中',
                translator: '2333',
                score: 4,
                price: '20元'
              }
            ]
          }
        ]
        // TODO: 实现全选
      }
    },
    created: function () {
      let body = JSON.stringify({taskid: this.$route.params.tid})
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetSquareTasks', { method: 'GET',
        headers,
        credentials: 'include',
        body: body })
      .then(function (response) {
        return response.json().then(function (data) {
          for (let task in data) {
            let tmptask = []
            tmptask.id = task['id']
            tmptask.title = task['title']
            tmptask.publishTime = task['publishTime']
            tmptask.ddlTime = task['ddlTime']
            tmptask.language = task['language']
            tmptask.tags = task['tags']
            tmptask.assignments = []
            for (let assignment of task) {
              let tmpassignment = []
              tmpassignment['order'] = assignment.order
              tmpassignment['description'] = assignment.description
              tmpassignment['translator'] = assignment.translator
              switch (assignment.status) {
                case 0:
                  tmpassignment['status'] = '未发布'
                  break
                case 1:
                  tmpassignment['status'] = '未认领'
                  break
                case 2:
                  tmpassignment['status'] = '进行中'
                  break
                case 3:
                  tmpassignment['status'] = '已完成'
                  tmpassignment['score'] = assignment.score
                  break
                case 4:
                  tmpassignment['status'] = '纠纷中'
                  tmpassignment['score'] = assignment.score
                  break
              }
              tmpassignment['price'] = assignment.price
              tmpassignment['submission'] = assignment.submission
              tmptask.assignments.push(tmpassignment)
            }
            that.tasklist.push(tmptask)
          }
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
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
  #chosen {
    text-align: left;
  }
  #ads {
    margin:50px;
  }
  .order {
    font-size: 20px;
    font-weight: 700;
    width:20px;
    color: #495060;
    margin: 0 8px 0 5px;
  }
  .words {
    margin-right: 10px;
  }
  .chosen_by {
    margin: 10px 0 5px 0;
    color: #80848f;
  }
  .description {
    margin-left:28px;
  }
  .card {
    margin-bottom: 10px;
  }
  li {
    text-align: left;
    margin-top:5px;
  }
  h2 {
    color: #1c2438;
    text-align: left;
  }
  h3 {
    font-size: 16px;
    color: #495060;
    text-align: left;
  }
  h4 {
    font-size: 14px;
    font-weight: 400;
    color: #80848f;
    text-align: left;
  }
  p {
    font-size: 14px;
    color: #495060;
    text-align: left;
  }

</style>
