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
                  <!-- <p v-if="a.status == '已完成'">任务评分:&nbsp;<Rate disabled v-model="a.score"></Rate></p> -->
                  <Button v-if="a.status == '已完成'" type="primary" @click="modalConfirm = true">fuck</Button>
                  <Modal title="确认任务" v-model="modalConfirm" :mask-closable="false" @on-ok="acceptAssignment(a)" :loading="loading">
                    <RadioGroup v-model="confirm">
                      <Radio label="accept"></Radio>
                      <Radio label="reject"></Radio>
                    </RadioGroup><br>
                    <Rate v-if="confirm === 'accept'" show-text allow-half v-model="valueCustomText">
                      <span style="color: #f5a623">{{ valueCustomText }}</span>
                    </Rate>
                    <Input v-else v-model="text" type="textarea" :rows="4" placeholder="请写出你的拒绝理由"></Input>
                  </Modal>
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
        <h3 id="right-info">任务信息</h3>
        <p>任务状态：{{ status }}</p><Button v-if="status == '待发布'" @click="publishTask">立即发布</Button>
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
        status: '已发布',
        description: '我是任务的描述',
        publishTime: '2017-3-1',
        ddlTime: '2017-5-10',
        language: '法语',
        assignments: [
          {
            id: 1,
            order: 1,
            description: '这个任务需要翻译我给出的pdf文档的第20-40页，注意主要人名的翻' +
            '译要与附录中的统一。完成情况好的话我一定会好评的。',
            status: '已完成',
            translator: '2333',
            score: 4,
            price: '20元',
            submission: '/2333/455',
            note: ''
          },
          {
            id: 2,
            order: 2,
            description: 'PartII PartII PartII PartII PartII PartII ',
            status: '进行中',
            translator: '2333',
            score: 4,
            price: '20元',
            submission: '/2333/455',
            note: ''
          }
        ],
        modalConfirm: false,
        confirm: 'accept',
        valueCustomText: 3,
        loading: true,
        text: ''
      }
    },
    created: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetTaskDetail?taskid=' + this.$route.params.tid, { method: 'GET',
        headers,
        credentials: 'include'})
      .then(function (response) {
        return response.json().then(function (data) {
          that.title = data['title']
          that.description = data['description']
          that.publishTime = Date(data['publishTime'])
          that.ddlTime = Date(data['ddlTime'])
          that.language = data['language']
          switch (data['status']) {
            case 0:
              that.status = '待发布'
              break
            case 1:
              that.status = '进行中'
              break
            case 2:
              that.status = '已结束'
              break
          }
          for (let assignment of data['assignment']) {
            let tmp = []
            tmp['id'] = assignment.id
            tmp['order'] = assignment.order
            tmp['description'] = assignment.description
            tmp['translator'] = assignment.translator
            switch (assignment.status) {
              case 0:
                tmp['status'] = '待发布'
                break
              case 1:
                tmp['status'] = '待领取'
                break
              case 2:
                tmp['status'] = '进行中'
                break
              case 3:
                tmp['status'] = '已完成'
                tmp['score'] = assignment.score
                break
              case 4:
                tmp['status'] = '纠纷中'
                tmp['score'] = assignment.score
                break
            }
            tmp['price'] = assignment.price
            tmp['submission'] = assignment.submission
            tmp['note'] = ''
            that.assignments.push(tmp)
          }
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
    },
    methods: {
      publishTask: function () {
        let body = JSON.stringify({taskid: this.$route.params.tid})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/PublishTask', { method: 'POST',
          headers,
          credentials: 'include',
          body: body})
        .then(function (response) {
          return response.json().then(function (data) {
            if (data.status) {
              that.status = '进行中'
              for (let assignment of that.assignments) {
                assignment.status = '待领取'
              }
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      acceptAssignment: function (assignment) {
        var result
        if (this.confirm === 'accept') {
          result = assignment.score = this.valueCustomText
        } else {
          result = assignment.note = this.text
        }
        let body = JSON.stringify({
          assignmentid: assignment.id,
          acceptance: this.confirm,
          result: result
        })
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/AcceptAssignment', {
          method: 'POST',
          headers,
          credentials: 'include',
          body: body
        })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data.status) {
              assignment.status = '已完成'
              assignment.scores = 0
              that.valueCustomText = 3
              that.text = ''
              that.modalConfirm = false
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin:20px auto 10px auto;
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
  #right-info {
    margin-bottom: 5px;
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
