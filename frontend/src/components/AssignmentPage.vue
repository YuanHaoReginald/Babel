<template>
  <div class="root">
    <div id="left">
      <div class="card">
        <Card dis-hover padding="0">
          <div id="task-info">
            <h2 id="task-title" @click="checkTaskDetail">{{ title }}<br></h2>
            <br>
            <div class="grey">
              发布者:&nbsp;<Avatar v-bind:src="owner.img_src" />
              {{ owner.name }}
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              任务状态:&nbsp;{{ assignment.status }}
            </div>
            <p>{{ description }}</p>
          </div>
          <div id="details">
            <p class="grey">详细信息:</p>
            <p>{{ assignment.description }}</p>
            <br>
            <span v-if="assignment.status == '待领取'">
              <Button type="primary"  @click="testConfirm = true">领取任务</Button>
            </span>
            <span v-if="assignment.status == '试译中'"></span>
            <span v-if="assignment.status == '进行中'">
              <div>
                <Upload
                  ref="upload"
                  :before-upload="handleBeforeUpload"
                  :on-success="handleSuccess"
                  :show-upload-list="false"
                  action="api/SubmitAssignment">
                  <Button type="ghost" icon="ios-cloud-upload-outline">Select the file to upload</Button>
                  <b class="grey" style="padding-left: 20px">{{ assignment.submission }}</b>
                </Upload>
                <div v-if="file !== null">
                  Upload file: {{ file.name }}
                  <Button type="text" @click="upload" :loading="loadingStatus">{{ loadingStatus ? 'Uploading' : 'Click to upload' }}</Button>
                  <Button shape="circle" icon="close" @click="cancel"></Button>
                </div>
              </div>
            </span>
            <span v-if="assignment.status == '已完成'" class="grey">
              任务评分:&nbsp;&nbsp;<Rate allow-half disbaled v-model="assignment.score"></Rate>
              <span v-if="assignment.hasDispute">
                <p v-if="assignment.disputeResult == 0"> 申诉状态：未完成（发生未知错误） </p>
                <p v-if="assignment.disputeResult == 1"> 申诉状态：管理员同意了您的申诉，评语：{{assignment.statement}} </p>
                <p v-if="assignment.disputeResult == 2"> 申诉状态：管理员拒绝了您的申诉，评语：{{assignment.statement}} </p>
              </span>
            </span>
            <span v-if="assignment.status == '纠纷中'">
              <span v-if="!assignment.hasDispute">
                <Button type="error" @click="modalArgue = true">申请投诉</Button>
                <Button type="success" @click="acceptResult">接受结果</Button>
                  <Modal v-model="modalArgue" title="申请投诉" @on-ok="argueResult">
                      <Input v-model="text" type="textarea" :rows="4" placeholder="请写出你的申诉理由"></Input>
                  </Modal>
              </span>
              <span v-if="assignment.hasDispute">
                <p>请耐心等待结果</p>
              </span>
            </span>
            <span v-if="assignment.status == '待评分'" class="grey">任务评分:&nbsp;&nbsp;<Rate allow-half disabled v-model="assignment.score"></Rate></span>
            <Modal title="试译" v-model="testConfirm" :mask-closable="false" :loading="loading">
              <p class="bottom-10">试译语段：</p>
              <p class="bottom-10">{{ testText }}</p>
              <p class="bottom-10">翻译结果：</p>
              <p class="bottom-10"><Input v-model="testResult" type="textarea" :rows="5" placeholder="请输入翻译结果"></Input></p>
              <div slot="footer" class="right">
                <Button type="ghost">取消</Button>
                <Button type="primary">提交</Button>
              </div>
            </Modal>
          </div>
        </Card>
      </div>
    </div>
    <div id="right">
      <div class="card">
        <Card dis-hover>
          <p slot="title" id="right-title">可能感兴趣的项目</p>
          <ul>
            <li v-for="r in recommendation" class="recommendation">
              <p>{{ r.title }}<span class="price">&nbsp;&nbsp;{{ r.price }}</span></p>
            </li>
          </ul>
        </Card>
      </div>
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
        owner: {
          name: '',
          img_src: ''
        },
        description: '',
        publishTime: '',
        ddlTime: '',
        language: '',
        assignment: {
          id: 0,
          hasDispute: false,
          disputeResult: 0,
          statement: '',
          description: '',
          status: '',
          translator: '',
          score: 0,
          price: '',
          submission: ''
        },
        recommendation: [
          {
            id: 2345,
            title: '法语报纸翻译',
            price: '200元'
          },
          {
            id: 2346,
            title: '《追忆似水年华》选段翻译',
            price: '50元'
          },
          {
            id: 2347,
            title: 'Enya歌词翻译',
            price: '70元'
          }
        ],
        file: null,
        loadingStatus: false,
        testConfirm: false,
        testText: '',
        testResult: '',
        modalArgue: false,
        text: ''
      }
    },
    created: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetAssignmentDetail?assignmentid=' + this.$route.params.aid, { method: 'GET',
        headers,
        credentials: 'include'})
      .then(function (response) {
        return response.json().then(function (data) {
          that.id = data['id']
          that.title = data['title']
          that.description = data['description']
          that.publishTime = Date(data['publishTime'])
          that.ddlTime = Date(data['ddlTime'])
          that.language = data['language']
          let assignment = data['assignment']
          that.assignment['id'] = assignment.id
          that.assignment['hasDispute'] = assignment.hasDispute
          that.assignment['disputeResult'] = assignment.disputeResult
          that.assignment['statement'] = assignment.statement
          that.assignment['translator'] = assignment.translator
          that.assignment['price'] = assignment.price
          that.assignment['submission'] = assignment.submission
          that.assignment['description'] = assignment.description
          switch (assignment.status) {
            case 0:
              that.assignment['status'] = '待发布'
              break
            case 1:
              that.assignment['status'] = '待认领'
              break
            case 2:
              that.assignment['status'] = '进行中'
              break
            case 3:
              that.assignment['status'] = '已完成'
              that.assignment['score'] = assignment.score
              break
            case 4:
              that.assignment['status'] = '纠纷中'
              that.assignment['score'] = assignment.score
              break
          }
          let owner = data['owner']
          that.owner.name = owner.name
          that.owner.img_src = owner.avatar
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
    },
    methods: {
      handleBeforeUpload (file) {
        this.file = file
        return false
      },
      handleSuccess (res, file) {
        console.log(res.url)
        this.assignment.submission = res.url
        this.file = null
      },
      upload () {
        this.loadingStatus = true
        this.$refs.upload.data = {assignmentid: this.$route.params.aid}
        this.$refs.upload.post(this.file)
        this.$Message.success('Success')
        this.loadingStatus = false
        this.file = null
      },
      cancel () {
        this.file = null
      },
      acceptResult () {
        let body = JSON.stringify({assignmentId: this.assignment['id']})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/AcceptResult', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data.status) {
              that.assignment['status'] = '已完成'
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      argueResult () {
        let body = JSON.stringify({assignmentId: this.assignment['id'], text: this.text})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/ArgueResult', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data.status) {
              that.assignment['hasDispute'] = true
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      checkTaskDetail: function () {
        this.$router.push('/task/' + this.id)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  div {
    text-align: left;
  }
  .root {
    margin:20px auto 10px auto;
    padding: 0 16px 0 16px;
    width:1000px;
  }
  #left {
    padding: 3px;
    float:left;
    width: 700px;
    line-height:250%;
  }
  #right{
    padding: 3px;
    width: 300px;
    margin-left: 703px;
  }
  .card {
    margin-bottom: 10px;
  }
  .recommendation {
    margin: 5px 0 10px 0;
    color: #1c2438;
  }
  .price {
    color: #80848f;
  }
  .grey {
    color: #80848f;
  }
  .right {
    text-align: right;
  }
  .bottom-10 {
    margin-bottom: 10px;
  }
  #right-title {
    margin-top: 3px;
    font-size: 15px;
    color: #1c2438;
  }
  #task-info {
    margin: 20px 0 20px 50px;
    width: 500px;
  }
  #details {
    margin: 20px 0 20px 50px;
    width: 500px;
  }
  #task-title {
    font-weight:200;
    font-size: 24px;
    color: #1c2438;
  }
  h2 {
    text-align: left;
  }
  p {
    font-size: 14px;
    text-align: left;
  }
  span {
    font-size: 14px;
  }

</style>
