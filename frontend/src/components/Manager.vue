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
      <ul v-if="checking === 'argues_notSolved'">
        <li v-for="a in argues.notSolved">
          <div class="card">
            <Card dis-hover>
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
      <ul v-if="checking === 'argues_solved'">
        <li v-for="a in argues.solved">
          <div class="card">
            <Card dis-hover>
              <p>翻译者：{{ a.argument_translator }}</p>
              <p>雇主：{{ a.argument_employer }}</p>
              <p v-if="a.result">同意</p><p v-else>不同意</p>
              <p>理由：{{ a.reason }}</p>
            </Card>
          </div>
        </li>
      </ul>
      <ul v-if="checking === 'licenses_notVerified'">
        <li v-for="l in licenses.notVerified">
          <div class="card">
            <Card dis-hover>
              <p>证书：{{ l.url }}</p>
              <p>类型：{{ l.type }}</p>
              <p>描述：{{ l.description }}</p>
              <div v-if="l.status == '待审核'" class="buttons">
                <Button type="primary" @click="setLicense(l, true)">有效</Button>
                <Button type="error" @click="setLicense(l, false)">无效</Button>
              </div>
            </Card>
          </div>
        </li>
      </ul>
      <ul v-if="checking === 'licenses_verified'">
        <li v-for="l in licenses.verified">
          <div class="card">
            <Card dis-hover>
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
              type: '',
              description: '1234567',
              url: 'http://www.cxyym.com/wp-content/uploads/2016/04/030a3bb51ba6ef4e0f7e73798a246655.png',
              result: null
            },
            {
              id: 20,
              status: '待审核',
              type: '',
              description: 'qwertyu',
              url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTinVcxgZ5o4TUaUzgfoUKGIuHMOCSnopg6lPs_WEjVZgZ7QBfc',
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
  #left {
    float:left;
  }
  #right{
    padding: 10px;
    margin-left: 250px;
  }
  .center {
    text-align: center;
  }
  .card {
    margin-bottom: 10px;
  }
  .buttons {
    margin: 10px;
  }
  .input {
    margin: 10px;
  }
</style>
