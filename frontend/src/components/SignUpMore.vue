<template>
  <div class="root">
    <Card dis-hover>
      <div class="card">
        <div class="title"><h2>完善个人信息</h2></div>
        <div class="box">
          <h3>上传头像：</h3>
          <Button type="primary" id="fileButton">选择文件</Button>
        </div>
        <div class="box">
          <h3>电话：</h3>
          <div class="input"><Input v-model="telephone"></Input></div>
        </div>
        <div class="box">
          <h3>邮箱：</h3>
          <div class="input"><Input v-model="email"></Input></div>
        </div>
        <div class="box">
          <h3>支付宝账号：</h3>
          <div class="input"><Input v-model="alipay"></Input></div>
        </div>
        <div class="box">
          <h3>微信号：</h3>
          <div class="input"><Input v-model="wechat"></Input></div>
        </div>
        <div class="box">
          <h3>上传证书：</h3>
          <Select v-model="language" style="width:200px;" id="languageSelect"  placeholder="<选择语言>">
            <Option v-for="item in languageList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
          <ul>
            <li v-for="l in licenseList[language]">
              <Row>
                <Col span="4"><h4>{{ l.label }}:</h4></Col>
                <Col span="6"><Button>上传证书扫描件</Button></Col>
              </Row>

            </li>
          </ul>

        </div>
        <div id="submitButton"><Button type="primary">提交修改</Button></div>
      </div>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'signUpMore',
    data () {
      return {
        telephone: '',
        email: '',
        alipay: '',
        wechat: '',
        language: '',
        languageList: [
          {
            value: 'English',
            label: '英语'
          },
          {
            value: 'Japanese',
            label: '日语'
          },
          {
            value: 'French',
            label: '法语'
          },
          {
            value: 'Russian',
            label: '俄语'
          },
          {
            value: 'Spanish',
            label: '西班牙语'
          }
        ],
        licenseList: {
          'English': [
            {
              value: 'cet4',
              label: '专业四级',
              src: ''
            },
            {
              value: 'cet8',
              label: '专业八级',
              src: ''
            }
          ],
          'French': [
            {
              value: 'cet4',
              label: '专业四级',
              src: ''
            },
            {
              value: 'cet8',
              label: '专业八级',
              src: ''
            }
          ],
        }
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
  #fileButton {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 600px;
  }
  #languageSelect {
    float:left;
    margin-top: 5px;
    margin-bottom: 20px;
    margin-right: 500px;
  }
  #submitButton {
    margin-top: 150px;
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
