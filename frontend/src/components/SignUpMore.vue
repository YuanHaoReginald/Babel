<!--This is for translator-->
<template>
  <div class="root">
    <Card dis-hover>
      <div class="card">
        <div class="title"><h2>完善个人信息</h2></div>
        <div class="box" id="head">
          <h3>上传头像：</h3>
          <div><div class="avatar-upload" v-if="avatar.url != ''">
            <template v-if="avatar.status === 'finished'">
              <img :src="avatar.url">
              <div class="upload-cover">
                <Icon type="ios-eye-outline" @click.native="handleView"></Icon>
                <Icon type="ios-trash-outline" @click.native="handleRemove(avatar)"></Icon>
              </div>
            </template>
            <template v-else>
              <Progress v-if="avatar.showProgress" :percent="avatar.percentage" hide-info></Progress>
            </template>
            <Modal title="View Image" v-model="visible">
              <img :src="avatar.url" v-if="visible" style="width: 100%">
            </Modal>
          </div>
          <div v-else>
            <Upload
              name="avatar"
              :data="{id: userid()}"
              :before-upload="handleBeforeUpload"
              :on-success="handleSuccess"
              :show-upload-list="false"
              :format="['jpg','jpeg','png']"
              :max-size="2048"
              :on-format-error="handleFormatError"
              :on-exceeded-size="handleMaxSize"
              type="drag"
              action="api/UploadAvatar"
              style="display: inline-block;width:58px;">
              <div style="width:58px;height:58px;line-height:58px;">
                <Icon type="camera" size="20"></Icon>
              </div>
            </Upload>
          </div></div>
        </div>
        <div class="box">
          <h3>电话：</h3>
          <div class="input"><Input v-model="telephone"></Input></div>
        </div>
        <div class="box">
          <h3>支付宝账号：</h3>
          <div class="input"><Input v-model="alipay"></Input></div>
        </div>
        <div class="box">
          <h3>微信号：</h3>
          <div class="input"><Input v-model="wechat"></Input></div>
        </div>
        <div class="box" v-if="translatorCheck">
          <h3>上传证书：</h3>
          <Select v-model="language" style="width:200px;" id="languageSelect"  placeholder="<选择语言>">
            <Option v-for="item in languageList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
          <ul>
            <li v-for="l in licenseList[language]">
              &nbsp;
              <Row>
                <Col span="4"><h4>{{ l.label }}:</h4></Col>
                <Col span="6">
                  <Upload
                    name="license"
                    :data="{language: language, type: l.value}"
                    :format="['jpg','jpeg','png']"
                    :max-size="10240"
                    :on-format-error="handleFormatError"
                    :on-exceeded-size="handleMaxSize"
                    type="drag"
                    action="api/UploadLicense">
                    上传证书扫描件
                  </Upload>
                </Col>
              </Row>
            </li>
          </ul>
        </div>
        <div id="submitButton"><Button type="primary" @click="modify_info">提交修改</Button></div>
      </div>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'signUpMore',
    data () {
      return {
        avatar: {
          url: '',
          showProgress: false
        },
        visible: false,
        telephone: null,
        alipay: null,
        wechat: null,
        language: null,
        languageList: [
          {
            value: 'English',
            label: '英语 / English'
          },
          {
            value: 'Japanese',
            label: '日语 / 日本語'
          },
          {
            value: 'French',
            label: '法语 / Français'
          },
          {
            value: 'Russian',
            label: '俄语 / русский'
          },
          {
            value: 'Spanish',
            label: '西班牙语 / Español'
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
          'Japanese': [
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
          'Russian': [
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
          'Spanish': [
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
          ]
        }
      }
    },
    methods: {
      modify_info: function () {
        let body = JSON.stringify({telephone: this.telephone,
          alipayNumber: this.alipay,
          wechatNumber: this.wechat})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/UserModify', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data['status']) {
              that.$Message.success('Modify successfully.')
            } else {
              that.$Message.warning('Modify Failed.')
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      handleView () {
        this.visible = true
      },
      handleRemove (file) {
        this.avatar.url = ''
      },
      handleBeforeUpload () {
        // this.avatar.url = ' '
      },
      handleSuccess (res, file) {
        console.log(res.url)
        this.avatar.url = res.url
        this.avatar.status = 'finished'
      },
      handleFormatError (file) {
        this.$Notice.warning({
          title: 'The file format is incorrect',
          desc: 'File format of ' + file.name + ' is incorrect, please select jpg or png.'
        })
      },
      handleMaxSize (file) {
        this.$Notice.warning({
          title: 'Exceeding file size limit',
          desc: 'File  ' + file.name + ' is too large, no more than 2M.'
        })
      },
      userid () {
        // return Number(sessionStorage.getItem('userid'))
        return Number(this.$store.state.userid)
      }
    },
    computed: {
      translatorCheck: function () {
        return this.$store.state.utype === 'translator'
      }
    },
    created: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/UserModify', { method: 'GET',
        headers,
        credentials: 'include'})
      .then(function (response) {
        return response.json().then(function (data) {
          // that.avatar.url = data['avatar']
          that.telephone = data['telephone']
          that.alipay = data['alipayNumber']
          that.wechat = data['wechatNumber']
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
    margin-top:30px;
    margin-left: auto;
    margin-right: auto;
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
  #head {
    text-align: left;
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
  .avatar-upload{
    width: 60px;
    height: 60px;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0,0,0,.2);
    margin-right: 4px;
  }
  .avatar-upload img{
    width: 100%;
    height: 100%;
  }
  .upload-cover{
      display: none;
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(0,0,0,.6);
  }
  .avatar-upload:hover .upload-cover{
      display: block;
  }
  .upload-cover i{
      color: #fff;
      font-size: 20px;
      cursor: pointer;
      margin: 0 2px;
  }
</style>
