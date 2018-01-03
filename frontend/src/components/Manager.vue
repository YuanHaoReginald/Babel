<template>
  <div id="root">
    <div id="left">
      <Menu :theme="theme" active-name="1">
        <MenuGroup title="申诉管理">
          <MenuItem name="1" @click.native="switchTo('argues_notSolved')">
            <Icon type="document-text"></Icon>
            尚未处理
          </MenuItem>
          <MenuItem name="2" @click.native="switchTo('argues_solved')">
            <Icon type="document-text"></Icon>
            已经处理
          </MenuItem>
        </MenuGroup>
        <MenuGroup title="证书审核">
          <MenuItem name="3" @click.native="switchTo('licenses_notVerified')">
            <Icon type="document-text"></Icon>
            尚未处理
          </MenuItem>
          <MenuItem name="4" @click.native="switchTo('licenses_verified')">
            <Icon type="document-text"></Icon>
            已经处理
          </MenuItem>
        </MenuGroup>
      </Menu>
    </div>
    <div id="right">
      <ul v-if="checking === 'argues_notSolved'" class="argue">
        <li v-for="a in argues.notSolved">
          <div class="card">
            <Card dis-hover padding="20">
              <p>翻译者：{{ a.argument_translator }}</p>
              <p>雇主：{{ a.argument_employer }}</p>
              <div v-if="a.status == '待审核'" class="buttons">
                <Button type="primary" @click="setArgue(a, true)">同意</Button>
                <Button type="error" @click="setArgue(a, false)">不同意</Button>
                <div class="input">
                  <Input v-model="a.reason" type="textarea" size="large"></Input>
                </div>
              </div>
            </Card>
          </div>
        </li>
      </ul>
      <ul v-if="checking === 'argues_solved'" class="argue">
        <li v-for="a in argues.solved">
          <div class="card">
            <Card dis-hover padding="20">
              <p v-if="a.result" class="status_text"><img src="../assets/yes.png" class="logo"><span>已同意</span></p>
              <p v-else class="status_text"><img src="../assets/no.png" class="logo"><span>已拒绝</span></p>
              <p>翻译者：{{ a.argument_translator }}</p>
              <p>雇主：{{ a.argument_employer }}</p>
              <p>理由：{{ a.reason }}</p>
            </Card>
          </div>
        </li>
      </ul>
      <ul v-if="checking === 'licenses_notVerified'" class="license">
        <li v-for="l in licenses.notVerified">
          <div class="card">
            <Card dis-hover padding="20">
              <p class="type_text">类型：{{ l.language }} | {{ l.type }}</p>
              <Card dis-hover  class="img">
                <div>
                  <img :src="l.url">
                </div>
              </Card>
              <div v-if="l.status == '待审核'" class="buttons">
                <Button type="primary" @click="setLicense(l, true)">有效</Button>
                <Button type="error" @click="setLicense(l, false)">无效</Button>
              </div>
            </Card>
          </div>
        </li>
      </ul>
      <ul v-if="checking === 'licenses_verified'">
        <li v-for="l in licenses.verified" class="license">
          <div class="card">
            <Card dis-hover padding="20">
              <p class="type_text">类型：{{ l.language }} | {{ l.type }}</p>
              <Card dis-hover  class="img">
                <div style="text-align:center">
                  <img :src="l.url">
                </div>
              </Card>
              <div v-if="l.status == '待审核'" class="buttons">
                <Button type="primary" @click="setLicense(l, true)">有效</Button>
                <Button type="error" @click="setLicense(l, false)">无效</Button>
              </div>
            </Card>
          </div><div class="card">
            <Card dis-hover  padding="20">
              <p>证书：{{ l.url }}</p>
              <p>类型：{{ l.type }}</p>
              <p>描述：{{ l.description }}</p>
              <p v-if="a.result">有效</p><p v-else>无效</p>
            </Card>
          </div>
        </li>
      </ul>
      <div class="center" v-if="total !== 0"><Page :total="total" show-elevator></Page></div>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        theme: 'light',
        checking: 'argues_notSolved',
        total: 100,
        argues: {
          notSolved: [
            {
              id: 1,
              status: '待审核',
              assignment_name: 'name',
              argument_translator: '我觉得没问题',
              argument_employer: '我觉得翻译很差不能给这么多',
              result: null,
              reason: ''
            },
            {
              id: 2,
              status: '待审核',
              assignment_name: 'name',
              argument_translator: '大家加油',
              argument_employer: '最胖',
              result: null,
              reason: ''
            }
          ],
          solved: []
        },
        licenses: {
          notVerified: [
            {
              id: 2,
              status: '待审核',
              type: '专业四级',
              language: '法语',
              url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTinVcxgZ5o4TUaUzgfoUKGIuHMOCSnopg6lPs_WEjVZgZ7QBfc',
              result: null
            },
            {
              id: 20,
              status: '待审核',
              type: '专业八级',
              language: '法语',
              url: 'http://www.cxyym.com/wp-content/uploads/2016/04/030a3bb51ba6ef4e0f7e73798a246655.png',
              result: null
            }
          ],
          verified: []
        }
      }
    },
    methods: {
      switchTo: function (mode) {
        this.checking = mode
        switch (mode) {
          case 'argues_notSolved':
            this.total = this.argues.notSolved.length
            break
          case 'argues_solved':
            this.total = this.argues.solved.length
            break
          case 'licenses_notVerified':
            this.total = this.licenses.notVerified.length
            break
          case 'licenses_verified':
            this.total = this.licenses.verified.length
            break
        }
      },
      setArgue: function (argue, result) {
        argue.status = '已审核'
        argue.result = result
        this.argues.solved[this.argues.solved.length] = argue
        for (var i = 0; i < this.argues.notSolved.length; ++i) {
          if (this.argues.notSolved[i] === argue) {
            this.argues.notSolved.splice(i, 1)
            break
          }
        }
        let body = JSON.stringify({disputeid: argue.id,
          result: result,
          statement: argue.reason
        })
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        fetch('api/SolveDispute', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      setLicense: function (license, result) {
        license.status = '已审核'
        license.result = result
        this.licenses.verified[this.licenses.verified.length] = license
        for (var i = 0; i < this.licenses.notVerified.length; ++i) {
          if (this.licenses.notVerified[i] === license) {
            this.licenses.notVerified.splice(i, 1)
            break
          }
        }
        let body = JSON.stringify({licenseid: license.id,
          result: result
        })
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        fetch('api/VerifyLicense', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      }
    },
    created: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      fetch('api/GetManager', { method: 'GET',
        headers,
        credentials: 'include' })
      .then(function (response) {
        return response.json().then(function (data) {
          this.total = data.DisputeList.length
          this.argues.notSolved = []
          for (let dispute of data.DisputeList) {
            this.argues.notSolved.push({
              id: dispute['id'],
              status: '待审核',
              assignment_name: dispute['assignment_name'],
              argument_translator: dispute['argument_translator'],
              argument_employer: dispute['argument_employer'],
              result: null,
              reason: ''
            })
          }
          this.licenses.notVerified = []
          for (let license of data.LicenseList) {
            this.licenses.notVerified.push({
              id: license['id'],
              status: '待审核',
              type: license['type'],
              description: license['description'],
              url: license['url'],
              result: null
            })
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
  p {
    text-align: left;
    font-size: 15px;
    color: #1c2438;
  }
  div {
    text-align: left;
  }
  span {
    margin: 0 0 150px 10px;
    color: #80848f;
  }
  #left {
    float:left;
  }
  #right{
    padding: 20px;
    margin-left: 245px;
  }
  .center {
    text-align: center;
  }
  .card {
    margin-bottom: 10px;
  }
  .argue .card {
    line-height:300%;
  }
  .license .card {
    line-height:400%;
  }
  .status_text {

  }
  .logo {
    width: 20px;
  }
  .buttons {
    margin: 10px 10px 10px 0;
  }
  .input {
    margin: 10px 10px 10px 0;
  }
  .img {
    width:355px;
    text-align:center;
  }
  .img div img {
    width: 320px;
  }
  .type_text {
    font-size: 15px;
  }
</style>
