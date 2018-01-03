<template>
  <div class="root">
    <div id="left">
      <div class="card">
        <Card dis-hover padding="0">
          <div id="task-info">
            <h2 id="task-title">{{ title }}<br></h2>
            <p>{{ description }}</p>
            <div class="grey">
              发布者：<Avatar v-bind:src="owner.img_src" />
              {{ owner.name }}
            </div>
          </div>
          <div id="details">
            <p class="grey">详细信息</p>
            <p>{{ assignment.description }}</p>
            <br>
            <span v-if="assignment.status == '待领取'"><Button type="primary" size="small">领取任务</Button></span>
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
            <span v-if="assignment.status == '已完成'"><b>任务评分</b>:&nbsp;<Rate v-model="assignment.score"></Rate></span>            
            <span v-if="assignment.status == '已完成'"><Button type="error" size="small">申请投诉</Button></span>
            <span v-if="assignment.status == '待评分'"><b>任务评分</b>:&nbsp;<Rate disabled v-model="assignment.score"></Rate></span>            
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
        title: '法语文件翻译任务',
        owner: {
          name: 'name2333',
          img_src: 'https://i.loli.net/2017/08/21/599a521472424.jpg'
        },
        description: '这是我比较着急的任务，主要是翻译一篇法语的论文。这是我' +
        '比较着急的任务，主要是翻译一篇法语的论文。这是我比较着急的任务，主要是翻译一篇法语的论文。',
        publishTime: '2017-3-1',
        ddlTime: '2017-5-10',
        language: '法语',
        assignment: {
          description: '这个任务需要翻译我给出的pdf文档的第20-40页，注意主要人名的翻' +
          '译要与附录中的统一。完成情况好的话我一定会好评的。',
          status: '进行中',
          translator: '2333',
          score: 4,
          price: '20元',
          submission: '/2333/455'
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
        loadingStatus: false
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
          that.title = data['title']
          that.description = data['description']
          that.publishTime = Date(data['publishTime'])
          that.ddlTime = Date(data['ddlTime'])
          that.language = data['language']
          let assignment = data['assignment']
          that.assignment['translator'] = assignment.translator
          that.assignment['price'] = assignment.price
          that.assignment['submission'] = assignment.submission
          that.assignment['description'] = assignment.description
          switch (assignment.status) {
            case 0:
              that.assignment['status'] = '未发布'
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

</style>
