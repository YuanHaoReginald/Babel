<template>
  <div class="root">
    <Card shadow>
      <div class="container">
        <img v-bind:src="headSrc" class="head">
        <h2>{{ username }}</h2>
        <Rate disabled show-text v-model="level">
          <span style="color: #f5a623">{{ level }}</span>
        </Rate>
        <Row id="scores">
          <Col span="6"><h4>经验：</h4></Col>
          <Col span="18">
            <Progress :percent="experiencePercent" hide-info></Progress>
            <h5>{{ experienceNumber }}/{{ maxExperience }}</h5>
          </Col>
        </Row>
      </div>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'userinfo',
    data () {
      return {
        username: '',
        email: '',
        headSrc: '',
        level: 0,
        experienceNumber: 0,
        maxExperience: 200
      }
    },
    computed: {
      experiencePercent: function () {
        return this.experienceNumber * 100 / this.maxExperience
      }
    },
    created: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetUserInfo', { method: 'GET',
        headers,
        credentials: 'include'})
      .then(function (response) {
        return response.json().then(function (data) {
          that.username = data['username']
          that.email = data['email']
          if (data['avatar'] !== '') {
            that.headSrc = data['avatar']
          }
          that.level = data['level']
          that.experienceNumber = data['experience']
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
    float: left;
    width: 300px;
    padding: 20px;
    margin-left: 180px;
  }
  .container {
    padding: 10px;
  }
  .head {
    width: 40%;
    margin: 10%;
  }
  #scores {
    padding: 5px;
  }
  h2 {
    color: #1c2438;
    padding: 5px;
  }

</style>
