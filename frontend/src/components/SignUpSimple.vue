<template>
  <div class="root">
    <div class="container">
    <div class="title"><h2>加入巴别塔</h2></div>
      <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="80">
        <FormItem label="用户名" prop="username">
          <Input type="username" v-model="formCustom.username"></Input>
        </FormItem>
        <FormItem label="密码" prop="passwd">
          <Input type="password" v-model="formCustom.passwd"></Input>
        </FormItem>
        <FormItem label="确认密码" prop="passwdCheck">
          <Input type="password" v-model="formCustom.passwdCheck"></Input>
        </FormItem>
        <FormItem label="邮箱" prop="email">
          <Input type="text" v-model="formCustom.email"></Input>
        </FormItem>
        <FormItem>
          <Button type="primary" @click="handleSubmit('formCustom')">Sign Up</Button>
          <Button type="ghost" @click="handleReset('formCustom')" style="margin-left: 8px">Reset</Button>
        </FormItem>
      </Form>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'sign_up_simple',
    data () {
      const reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      const validateUsername = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter your username'))
        } else {
          var checkUsername
          const headers = new Headers({
            'Content-Type': 'application/json'
          })
          fetch('api/UsernameCheck', {
            method: 'POST',
            headers,
            credentials: 'include',
            body: JSON.stringify({username: value})
          }).then(function (response) {
            return response.json().then(function (data) {
              checkUsername = data.status
              if (checkUsername) {
                callback(new Error('This username has been picked.'))
              } else {
                callback()
              }
            })
          }).catch(function (ex) {
            alert('Network Error')
          })
        }
      }
      const validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter your password'))
        } else {
          if (this.formCustom.passwdCheck !== '') {
            this.$refs.formCustom.validateField('passwdCheck')
          }
          callback()
        }
      }
      const validatePassCheck = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter your password again'))
        } else if (value !== this.formCustom.passwd) {
          callback(new Error('The two input passwords do not match!'))
        } else {
          callback()
        }
      }
      const validateEmail = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('Email cannot be empty'))
        }
        if (!reg.test(value)) {
          return callback(new Error('Please input a valid e-mail address.'))
        } else {
          callback()
        }
      }
      return {
        formCustom: {
          username: '',
          passwd: '',
          passwdCheck: '',
          email: ''
        },
        ruleCustom: {
          username: [
            { validator: validateUsername, trigger: 'blur' }
          ],
          passwd: [
            { validator: validatePass, trigger: 'blur' }
          ],
          passwdCheck: [
            { validator: validatePassCheck, trigger: 'blur' }
          ],
          email: [
            { validator: validateEmail, trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      handleSubmit (name) {
        let body = JSON.stringify({username: this.formCustom.username,
          password: this.formCustom.passwd,
          email: this.formCustom.email,
          utype: this.$route.params.utype})
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/UserSignUp', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data['id'] === 0) {
              that.$Message.warning('The username or e-mail address has already been picked, please retry.')
            } else {
              sessionStorage.setItem('userid', data.id)
              sessionStorage.setItem('utype', that.$route.params.utype)
              that.$store.commit('login', {'userid': data.id, 'utype': that.$route.params.utype, 'username': that.formCustom.username})
              that.$router.push('/signupmore')
            }
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      handleReset (name) {
        this.$refs[name].resetFields()
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin-top: 100px;
    margin-left: auto;
    margin-right: auto;
  }
  .container {
    margin: 0 auto;
    width:400px;
  }
  .title {
    width:400px;
    margin-bottom: 20px;
  }
  .input {
    margin: 0;
  }
  h2 {
    color: #1c2438;
    text-align: left;
    font-size:40px;
  }
  h3 {
    color: #1c2438;
    text-align: left;
  }

</style>
