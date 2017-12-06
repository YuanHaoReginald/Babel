<template>
  <div class="root">
    <div id="left">
      <div class="card"><Card dis-hover><h2>{{ title }}</h2></Card></div>
      <div class="card"><Card dis-hover padding="0">
        <div id="taskTitle"><h3 style="text-align: left;">细分任务详情</h3></div>
        <ul>
          <li v-for="a in assignments">
            <Card>
              <Row>
                <Col span="2"><h3>{{ a.order }}</h3></Col>
                <Col span="22">
                  <p>任务状态: {{ a.status }}</p>
                  <p v-if="a.status == '已完成'">任务评分:&nbsp;<Rate disabled v-model="a.score"></Rate></p>
                  <p>任务描述： </p>
                  <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ a.description }}</p>
                </Col>
              </Row>
            </Card>
          </li>
        </ul>
      </Card></div>
    </div>
    <div id="right">
      <div class="card"><Card dis-hover>
        <h3 style="margin-bottom: 5px;">任务信息</h3>
        <p>任务描述：{{ description }}</p>
        <p>任务语言：{{ language }}</p>
        <p>发布时间：{{ publishTime }}</p>
        <p>截止时间：{{ ddlTime }}</p>
      </Card></div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'taskpage',
    data () {
      return {
        title: '法语文件翻译任务',
        description: '我是任务的描述',
        publishTime: '2017-3-1',
        ddlTime: '2017-5-10',
        language: '法语',
        assignments: [
          {
            order: 1,
            description: '这个任务需要翻译我给出的pdf文档的第20-40页，注意主要人名的翻' +
            '译要与附录中的统一。完成情况好的话我一定会好评的。',
            status: '已完成',
            translator: '2333',
            score: 4,
            price: '20元',
            submission: '/2333/455'
          },
          {
            order: 2,
            description: 'PartII PartII PartII PartII PartII PartII ',
            status: '进行中',
            translator: '2333',
            score: 4,
            price: '20元',
            submission: '/2333/455'
          }
        ]
      }
    },
    created: function () {
      let body = JSON.stringify({taskid: this.$route.params.tid})
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetTaskDetail', { method: 'GET',
        headers,
        credentials: 'include',
        body: body })
      .then(function (response) {
        return response.json().then(function (data) {
          that.title = data['title']
          that.description = data['description']
          that.publishTime = data['publishTime']
          that.ddlTime = data['ddlTime']
          that.language = data['language']
          for (let assignment of data) {
            let tmp = new Array()
            tmp['order'] = assignments.order
            tmp['description'] = assignment.description
            tmp['translator'] = assignment.translator
            switch (assignment.status) {
              case 0:
                tmp['status'] = '未发布'
                break;
              case 1:
                tmp['status'] = '未认领'
                break;
              case 2:
                tmp['status'] = '进行中'
                break;
              case 3:
                tmp['status'] = '已完成'
                tmp['score'] = assignment.score
                break;
              case 4:
                tmp['status'] = '纠纷中'
                tmp['score'] = assignment.score
                break;
            }
            tmp['price'] = price
            tmp['submission'] = submission
            that.assignments.push(tmp)
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
