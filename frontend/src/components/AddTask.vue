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
          <div id="datepicker"><DatePicker type="date" placeholder="Select date" style="width: 200px"></DatePicker></div>
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
          <Button type="primary" id="fileButton">选择文件</Button>
        </div>
        <div class="box">
          <h3>标签：</h3>
          <div class="input"><Input v-model="tagsStr" placeholder="请输入标签名称，各标签以#分隔"></Input></div>
        </div>
        <div class="box">
          <h3>任务描述：</h3>
          <div class="input"><Input v-model="description" type="textarea"></Input></div>
        </div>
      </div>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'addTask',
    data () {
      return {
        title: '',
        language:'',
        level:0,
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
            value: '专业四级',
            label: '专业四级'
          },
          {
            value: '专业八级',
            label: '专业八级'
          }
        ],
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
</style>
