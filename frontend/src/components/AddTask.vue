<template>
  <div class="root">
    <Card dis-hover>
      <div class="card">
        <div class="title"><h2>创建新任务</h2></div>
        <div class="box">
          <h3>任务标题：</h3>
          <div class="input"><Input v-model="title"></Input></div>
        </div>
        <div class="box">
          <h3>任务语言：</h3>
          <Select v-model="language" style="width:200px;" id="languageSelect">
            <Option v-for="item in languageList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </div>
        <div class="box">
          <h3>截止时间：</h3>
          <div id="datepicker"><DatePicker v-model="ddlTime" type="date" placeholder="Select date" style="width: 200px"></DatePicker></div>
        </div>
        <div class="box">
          <h3>译者资质：</h3>
          <Select v-model="license" style="width:200px;" id="licenseSelect">
            <Option v-for="item in licenseList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </div>
        <div class="box">
          <h3>译者等级要求：</h3>
            <div class="rate">
              <Rate allow-half v-model="level"></Rate>
            </div>
        </div>
        <div class="box">
          <h3>任务文件：</h3>
          <Upload
            ref="upload"
            name="file"
            :before-upload="handleBeforeUpload"
            :data="{id: task_id}"
            action="api/UploadTaskFile">
            <Button type="ghost" icon="ios-cloud-upload-outline" id="fileButton">选择文件</Button>
          </Upload>
          <div v-if="file !== null">
            Upload file: {{ file.name }}
            <Button type="text" :loading="loadingStatus">{{ loadingStatus ? 'Uploading' : 'Ready' }}</Button>
          </div>
        </div>
        <div class="box">
          <h3>标签：</h3>
          <div class="input"><Input v-model="tagsStr" placeholder="请输入标签名称，各标签以#分隔"></Input></div>
        </div>
        <div class="box">
          <h3>任务总体描述：</h3>
          <div class="input"><Input v-model="description" type="textarea"></Input></div>
        </div>
        <div class="box">
          <h3>任务切分：</h3>
          <ul>
            <li v-for="a in assignments">
              <Row>
                <Col span="1">
                  <div id="addTaskButton" v-if="a.order == assignment_num">
                  <Button type="primary" size="small" shape="circle" icon="plus" @click="addAssignment">
                  </Button>
                  </div>
                  <div v-else>
                    <h4>&nbsp;</h4>
                  </div>
                </Col>
                <Col span="4"><div class="task_text"><h4>细分任务{{ a.order }}:</h4></div></Col>
                <Col span="17"><div class="input_assignment"><Input v-model="a.text" type="textarea"></Input></div></Col>
                <Col span="2"><div class="delete_button" v-if="assignment_num > 1"><Button type="ghost" @click="deleteAssignment(a.order)">删除</Button></div></Col>
              </Row>
            </li>
          </ul>
        </div>
        <div id="submitButton"><Button type="primary" @click="create_task">创建任务</Button></div>
      </div>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'addTask',
    data () {
      return {
        task_id: 0,
        title: null,
        language: null,
        license: null,
        description: null,
        tagsStr: null,
        ddlTime: null,
        level: 0,
        file: null,
        loadingStatus: false,
        languageList: [
          {
            value: 'English',
            label: 'English'
          },
          {
            value: 'Japanese',
            label: 'Japanese'
          },
          {
            value: 'French',
            label: 'French'
          },
          {
            value: 'Russian',
            label: 'Russian'
          },
          {
            value: 'Spanish',
            label: 'Spanish'
          }
        ],
        licenseList: [
          {
            value: 'cet4',
            label: '专业四级'
          },
          {
            value: 'cet8',
            label: '专业八级'
          }
        ],
        assignment_num: 1,
        assignments: [
          {
            order: 1,
            text: ''
          }
        ]
      }
    },
    methods: {
      handleBeforeUpload (file) {
        this.file = file
        return false
      },
      handleUpload () {
        console.log(this.task_id)
        this.loadingStatus = true
        this.$refs.upload.post(this.file)
        this.file = null
        this.loadingStatus = false
      },
      addAssignment () {
        this.assignment_num = this.assignment_num + 1
        this.assignments.push(
          {
            order: this.assignment_num,
            text: ''
          }
        )
      },
      deleteAssignment (num) {
        --num
        this.assignment_num = this.assignment_num - 1
        this.assignments.splice(num, 1)
        while (num < this.assignment_num) {
          this.assignments[num].order = ++num
        }
      },
      create_task: function () {
        let body = JSON.stringify({title: this.title,
          language: this.language,
          license: this.license,
          description: this.description,
          tags: this.tagsStr,
          ddlTime: Date.parse(this.ddlTime),
          level: this.level,
          assignments: this.assignments})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/CreateTask', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            that.task_id = data.task_id
            that.handleUpload()
            that.$router.push('/task/' + data.task_id)
          })
        }).catch(function (ex) {
          that.$Message.warning('Create new Task Failed.')
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin-top:30px;
    margin-left: 250px;
    width:750px;
  }
  .card {
    padding:15px;
  }
  .box {
    margin: 15px;
  }
  .title {
    margin:10px 0 20px 0;
  }
  .input {
    margin-top:5px;
  }
  .input_assignment {
    margin-top: 5px;
    width: 450px;
  }
  .task_text {
    text-align: center;
    margin:10px;
  }
  .delete_button {
    margin-top: 5px;
  }
  #languageSelect {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 500px;
  }
  #licenseSelect {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 500px;
  }
  #fileButton {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 600px;
  }
  #datepicker {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 600px;
  }
  #addTaskButton {
    margin: 10px;
  }
  #submitButton {
    margin-top: 50px;
  }
  .rate {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 520px;
  }
  h2 {
    color: #1c2438;
    text-align: left;
  }
  h3 {
    font-size: 16px;
    color: #80848f;
    text-align: left;
  }
  h4 {
    color: #80848f;
  }
  li {
    margin-bottom: 20px;
  }
</style>
