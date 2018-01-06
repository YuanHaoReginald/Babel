<template>
  <div class="root">
    <div id="left">
      <div class="card"><Card dis-hover><h2>{{ title }}</h2></Card></div>
      <div class="card"><Card dis-hover padding="0">
        <div id="taskTitle"><h3 style="text-align: left;">细分任务详情</h3></div>
        <ul>
          <li v-for="a in assignments">
            <Card>
              <Row class="text">
                <Col span="2"><h3>{{ a.order }}</h3></Col>
                <Col span="22" class="left">
                  <p>任务状态: {{ a.status }}</p>
                  <p>任务描述: </p>
                  <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{ a.description }}</p>
                  <p v-if="(a.status == '进行中' || a.status == '已完成' || a.status == '纠纷中') && isowner">翻译结果:&nbsp;<a :href="DownloadAssignment(a.submission)">{{ a.submission }}</a></p>
                  <div class="button">
                    <Button type="primary" @click="callConfirm(a)" v-if="a.status == '进行中' && isowner">任务验收</Button>
                    <Button type="primary" v-if="a.status == '试译中' && isowner" @click="callTestConfirm(a)" >查看试译结果</Button>
                    <Button type="primary" @click="pickup(a)" v-if="a.status == '待领取' && !isowner">领取任务</Button>
                    <span v-if="a.status == '已完成'">任务评分:&nbsp;<Rate allow-half disabled v-model="a.score"><span class="orange">{{ a.score }}</span></Rate></span>
                  </div>
                  <span v-if="a.status == '纠纷中' && isowner">
                    <p v-if="!a.hasDispute">请耐心等待翻译者回应</p>
                    <p v-if="a.hasDispute">请耐心等待管理员处理</p>
                  </span>
                  <span v-if="a.status == '已完成' && isowner && a.hasDispute">
                    <p v-if="a.disputeResult == 0"> 申诉状态：未完成（发生未知错误） </p>
                    <p v-if="a.disputeResult == 1"> 申诉状态：管理员同意了翻译者的申诉，评语：{{a.statement}} </p>
                    <p v-if="a.disputeResult == 2"> 申诉状态：管理员拒绝了翻译者的申诉，评语：{{a.statement}} </p>
                  </span>
                </Col>
              </Row>
            </Card>
          </li>
        </ul>
        <Modal title="试译结果" v-model="testConfirm" :mask-closable="false" :loading="loading">
          <p class="bottom-10">试译语段：</p>
          <p class="bottom-10">{{ testText }}</p>
          <p class="bottom-10">翻译结果：</p>
          <p class="bottom-10">{{ testResult }}</p>
          <div slot="footer">
            <Button type="error" @click="responseTestResult(false)">不通过</Button>
            <Button type="primary" @click="responseTestResult(true)">通过</Button>
          </div>
        </Modal>
        <Modal title="确认任务" v-model="modalConfirm" :mask-closable="false" @on-ok="acceptAssignment" :loading="loading">
          <RadioGroup v-model="confirm" class="options">
            <Radio label="accept"></Radio>
            <Radio label="reject"></Radio>
          </RadioGroup><br>
          <Rate v-if="confirm === 'accept'" show-text allow-half v-model="valueCustomText">
            <span class="orange">{{ valueCustomText }}</span>
          </Rate>
          <Input v-else v-model="text" type="textarea" :rows="4" placeholder="请写出你的拒绝理由"></Input>
        </Modal>
      </Card></div>
    </div>
    <div id="right" :class="rightFixed === true ? 'isFixed' :''">
      <div class="card"><Card dis-hover>
        <h3 id="right-info">任务信息</h3>
        <p>任务状态：{{ status }}</p>
        <p>任务描述：{{ description }}</p>
        <p>任务语言：{{ language }}</p>
        <p>资质要求：{{ requirementLicense }}</p>
        <p>发布时间：{{ publishTime }}</p>
        <p>截止时间：{{ ddlTime }}</p>
        <p>要求译者等级：&nbsp;<Rate allow-half disabled v-model="requirementLevel"></Rate></p>
        <p>任务文件：<a :href="DownloadTask(taskFile)">{{ taskFile }}</a></p>
        <Button v-if="status == '待发布'" @click="publishTask"  type="info">立即发布</Button>
      </Card></div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'taskpage',
    data () {
      return {
        id: 0,
        title: '',
        status: '',
        description: '',
        publishTime: '',
        ddlTime: '',
        language: '',
        requirementLicense: '',
        requirementLevel: 0,
        taskFile: '',
        employerId: 0,
        assignments: [],
        modalConfirm: false,
        testConfirm: false,
        confirm: 'accept',
        valueCustomText: 0,
        loading: true,
        text: '',
        testText: '',
        testResult: '',
        currentAssignment: null,
        rightFixed: false
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
          that.id = data['id']
          that.title = data['title']
          that.description = data['description']
          that.publishTime = Date(data['publishTime'])
          that.ddlTime = Date(data['ddlTime'])
          if (data['requirementLicense'] === 4) {
            that.requirementLicense = '专业四级'
          } else {
            that.requirementLicense = '专业八级'
          }
          that.requirementLevel = data['requirementLevel']
          // that.language = data['language']
          switch (data['language']) {
            case 0:
              that.language = '中文'
              break
            case 1:
              that.language = '英语'
              break
            case 2:
              that.language = '日语'
              break
            case 3:
              that.language = '法语'
              break
            case 4:
              that.language = '俄语'
              break
            case 5:
              that.language = '西班牙语'
              break
          }
          that.taskFile = data['fileUrl']
          that.employerId = data['employerId']
          that.testText = data['testText']
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
            tmp['hasDispute'] = assignment.hasDispute
            tmp['disputeResult'] = assignment.disputeResult
            tmp['statement'] = assignment.statement
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
              case 10:
                tmp['status'] = '试译中'
                break
            }
            tmp['price'] = assignment.price
            tmp['submission'] = assignment.submission
            tmp['note'] = ''
            tmp['testResult'] = assignment.testResult
            that.assignments.push(tmp)
          }
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
    },
    computed: {
      isowner: function () {
        return this.$store.state.utype === 'employer' && this.employerId === this.$store.state.userid
      }
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
      acceptAssignment: function () {
        var result
        if (this.confirm === 'accept') {
          result = this.currentAssignment.score = this.valueCustomText
        } else {
          result = this.currentAssignment.note = this.text
          this.currentAssignment.score = 0
        }
        let body = JSON.stringify({
          assignmentid: this.currentAssignment.id,
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
              if (that.confirm === 'accept') {
                that.currentAssignment.status = '已完成'
              } else {
                that.currentAssignment.status = '纠纷中'
              }
              that.valueCustomText = 3
              that.text = ''
              that.modalConfirm = false
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      DownloadAssignment: function (submission) {
        return 'api/FileDownload?type=assignments&filename=' + submission
      },
      DownloadTask: function (submission) {
        return 'api/FileDownload?type=tasks&filename=' + submission
      },
      pickup: function (assignment) {
        let body = JSON.stringify({task_id: this.id, assignment_order: assignment.order})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/PickupAssignment', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data.translator === that.$store.state.username) {
              that.$Message.success('Receive Assignment Success')
              assignment.status = '进行中'
              assignment.translator = that.$store.state.username
              that.$forceUpdate()
            } else {
              that.$Message.warning('The Assignment has been picked by another translator')
            }
          })
        }).catch(function (ex) {
          console.log(ex)
          alert('Network Error')
        })
      },
      responseTestResult: function (result) {
        let body = JSON.stringify({assignment_id: this.currentAssignment.id, result: result})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/ResponseTestResult', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (result) {
              that.currentAssignment.status = '进行中'
            } else {
              that.currentAssignment.status = '待领取'
              that.currentAssignment.translator = ''
              that.testConfirm = false
            }
          })
        }).catch(function (ex) {
          console.log(ex)
          alert('Network Error')
        })
      },
      callConfirm: function (assignment) {
        this.currentAssignment = assignment
        this.modalConfirm = true
      },
      callTestConfirm: function (assignment) {
        this.currentAssignment = assignment
        this.testResult = this.currentAssignment.testResult
        this.testConfirm = true
      },
      handleScroll () {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        var offsetTop = document.querySelector('#right').offsetTop
        if (scrollTop > offsetTop && !this.rightFixed) {
          this.rightFixed = true
        } else if (scrollTop < 80 && this.rightFixed) {
          this.rightFixed = false
        }
      }
    },
    mounted: function () {
      window.addEventListener('scroll', this.handleScroll)
    },
    destroyed: function () {
      window.removeEventListener('scroll', this.handleScroll)
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
    line-height:200%;
  }
  .button {
    margin-top: 10px;
  }
  .card {
    margin-bottom: 10px;
  }
  .orange {
    color: #f5a623;
  }
  .left {
    text-align: left;
  }
  .text {
    line-height:200%;
  }
  .options {
    margin-bottom: 10px;
  }
  .bottom-10 {
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
    font-weight: 200;
    text-align: left;
  }
  h3 {
    font-size: 16px;
    color: #495060;
    font-weight: 200;
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
  .isFixed {
    position: fixed;
    top: 0;
    z-index: 999;
  }
</style>
