<template>
  <div class="root">
    <div id="left">
      <div v-if="tasklist.length">
        <div class="card" v-for="task in tasklist" v-if="taskFilter(task)">
          <Card dis-hover>
            <div class="task">
              <h4>标签：{{ toStr(task.tags) }}</h4>
              <h2 @click="checkTaskDetail(task.id)">{{ task.title }}</h2>
              <ul>
                <li v-for="a in task.assignments" v-if="assignmentFilter(a)">
                  <span class="order">{{ a.order }}</span>
                  <span class="words"><b>报酬</b>：{{ a.price }}元</span>
                  <span class="words"><b>状态</b>： {{ a.status }}</span>
                  <span v-if="a.status == '已完成'"><b>任务评分</b>:&nbsp;<Rate allow-half disabled v-model="a.score"></Rate></span>
                  <span v-if="canPickup(a)"><Button type="primary" size="small" @click="pickup(task, a)">领取任务</Button></span>
                  <p class="description"><b>详情</b>： {{ a.description }}</p>
                </li>
              </ul>
            </div>
          </Card>
        </div>
        <Modal title="请试译" v-model="testConfirm" :mask-closable="false" @on-ok="submitTestResult" :loading="loading">
          <p class="bottom-10">试译语段：</p>
          <p class="bottom-10">{{ testText }}</p>
          <p class="bottom-10">翻译结果：</p>
          <br>
          <Input v-model="testResult" type="textarea" :rows="4" placeholder="请写出你的翻译结果"></Input>
        </Modal>
      </div>
      <div v-else>
        对不起，暂时没找到已发布的任务哦~
      </div>
    </div>
    <div id="right" :class="rightFixed === true ? 'isFixed' :''">
      <div class="card" id="chosen"><Card dis-hover>
        <h3 style="margin-bottom: 5px;">筛选任务</h3>
        <div class="chosen_by">按标签</div>
        <CheckboxGroup v-model="chosen_tags">
          <Checkbox label="全选"></Checkbox>
          <Checkbox label="公文"></Checkbox>
          <Checkbox label="文学"></Checkbox>
          <Checkbox label="法律"></Checkbox>
          <Checkbox label="艺术"></Checkbox>
        </CheckboxGroup>
        <div class="chosen_by">按语言</div>
        <CheckboxGroup v-model="chosen_languages">
          <Checkbox label="全选"></Checkbox>
          <Checkbox label="英语"></Checkbox>
          <Checkbox label="法语"></Checkbox>
          <Checkbox label="德语"></Checkbox>
          <Checkbox label="俄语"></Checkbox>
          <Checkbox label="日语"></Checkbox>
          <Checkbox label="西班牙语"></Checkbox>
        </CheckboxGroup>
        <div class="chosen_by">按价格</div>
        <CheckboxGroup v-model="chosen_price">
          <Checkbox label="全选"></Checkbox>
          <Checkbox label="0-30元"></Checkbox>
          <Checkbox label="30-100元"></Checkbox>
          <Checkbox label="100元以上"></Checkbox>
        </CheckboxGroup>
      </Card></div>
      <div class="card"><Card dis-hover>
        <h3>ADs</h3>
        <div id="ads">此广告位常年招租</div>
      </Card></div>
    </div>
    <BackTop></BackTop>
  </div>
</template>

<script>
  import { Checkbox } from 'iview'
  export default {
    components: {Checkbox},
    name: 'square',
    data () {
      return {
        theme: 'light',
        chosen_tags: [],
        chosen_languages: [],
        chosen_price: [],
        testText: '',
        testResult: '',
        testConfirm: false,
        tasklist: [],
        rightFixed: false
      }
    },
    methods: {
      pickup: function (task, assignment) {
        if (task.testText === '') {
          let body = JSON.stringify({task_id: task.id, assignment_order: assignment.order})
          const headers = new Headers({
            'Content-Type': 'application/json'
          })
          let that = this
          fetch('api/PickupAssignment', { method: 'POST',
            headers,
            credentials: 'include',
            body: body })
          .then(function (response) {
            return response.json().then(function (data) {
              if (data.status) {
                that.$Message.success('Receive Assignment Success')
                assignment.status = '进行中'
                assignment.translator = that.$store.state.username
                that.$forceUpdate()
              } else {
                that.$Message.warning(data.reason)
              }
            })
          }).catch(function (ex) {
            alert('Network Error')
          })
        } else {
          this.testConfirm = true
          this.testText = task.testText
          this.currentTask = task
          this.currentAssignment = assignment
        }
      },
      submitTestResult: function () {
        let body = JSON.stringify({
          task_id: this.currentTask.id,
          assignment_order: this.currentAssignment.order,
          testResult: this.testResult
        })
        const headers = new Headers({
          'Content-Type': 'application/json'
        })
        let that = this
        fetch('api/SubmitTestResult', { method: 'POST',
          headers,
          credentials: 'include',
          body: body })
        .then(function (response) {
          return response.json().then(function (data) {
            if (data.translator === that.$store.state.username) {
              that.$Message.success('Receive Assignment Success')
              that.currentAssignment.status = '试译中'
              that.currentAssignment.translator = that.$store.state.username
              that.$forceUpdate()
            } else {
              that.$Message.warning('The Assignment has been picked by another translator')
            }
            that.testConfirm = false
            that.testResult = ''
          })
        }).catch(function (ex) {
          alert('Network Error')
        })
      },
      toStr: function (tags) {
        let str = ''
        for (let i = 0; i < tags.length; i++) {
          str = str + ' ' + tags[i]
        }
        return str
      },
      checkTaskDetail: function (taskid) {
        this.$router.push('/task/' + taskid)
      },
      canPickup: function (assignment) {
        return assignment.status === '待领取' && this.$store.state.utype === 'translator'
      },
      taskFilter (task) {
        var flag = 0
        if (!this.chosen_languages.length) {
          flag++
        } else {
          for (let language of this.chosen_languages) {
            if (language === '全选' || language === task.language) {
              flag++
              break
            }
          }
        }
        if (!this.chosen_tags.length) {
          flag++
        } else {
          for (let tag of this.chosen_tags) {
            if (tag === '全选' || task.tags.indexOf(tag) > -1) {
              flag++
              break
            }
          }
        }
        if (!this.chosen_price.length) {
          flag++
        } else {
          var priceflag = false
          for (let assignment of task.assignments) {
            for (let price of this.chosen_price) {
              if (price === '全选') {
                priceflag++
              } else {
                switch (price) {
                  case '0-30元':
                    if (assignment.price >= 0 && assignment.price <= 30) {
                      priceflag = true
                    }
                    break
                  case '30-100元':
                    if (assignment.price >= 30 && assignment.price <= 100) {
                      priceflag = true
                    }
                    break
                  case '100元以上':
                    if (assignment.price >= 100) {
                      priceflag = true
                    }
                    break
                }
              }
              if (priceflag) {
                break
              }
            }
            if (priceflag) {
              flag++
              break
            }
          }
        }
        return flag === 3
      },
      assignmentFilter (assignment) {
        if (!this.chosen_price.length) {
          return true
        }
        for (let price of this.chosen_price) {
          if (price === '全选') {
            return true
          } else {
            switch (price) {
              case '0-30元':
                if (assignment.price >= 0 && assignment.price <= 30) {
                  return true
                }
                break
              case '30-100元':
                if (assignment.price >= 30 && assignment.price <= 100) {
                  return true
                }
                break
              case '100元以上':
                if (assignment.price >= 100) {
                  return true
                }
                break
            }
          }
        }
        return false
      },
      handleScroll () {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        var offsetTop = document.querySelector('#right').offsetTop
        if (scrollTop > offsetTop && !this.rightFixed) {
          this.rightFixed = true
        } else if (scrollTop < 80 && this.rightFixed) {
          this.rightFixed = false
        }
      }
    },
    created: function () {
      var url = 'api/GetSquareTasks'
      if (this.$route.params.keyword !== undefined) {
        url += '?keyword=' + this.$route.params.keyword
      }
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch(url, {
        method: 'GET',
        headers,
        credentials: 'include'
      })
      .then(function (response) {
        return response.json().then(function (data) {
          that.tasklist = []
          for (let task of data.taskList) {
            let tmptask = []
            tmptask.id = task['id']
            tmptask.title = task['title']
            tmptask.publishTime = task['publishTime']
            tmptask.ddlTime = task['ddlTime']
            // tmptask.language = task['language']
            switch (task['language']) {
              case 0:
                tmptask.language = '中文'
                break
              case 1:
                tmptask.language = '英语'
                break
              case 2:
                tmptask.language = '日语'
                break
              case 3:
                tmptask.language = '法语'
                break
              case 4:
                tmptask.language = '俄语'
                break
              case 5:
                tmptask.language = '西班牙语'
                break
            }
            tmptask.tags = task['tags']
            tmptask.testText = task['testText']
            tmptask.assignments = []
            for (let assignment of task['assignment']) {
              let tmpassignment = []
              tmpassignment['order'] = assignment.order
              tmpassignment['description'] = assignment.description
              tmpassignment['translator'] = assignment.translator
              switch (assignment.status) {
                case 0:
                  tmpassignment['status'] = '待发布'
                  break
                case 1:
                  tmpassignment['status'] = '待领取'
                  break
                case 2:
                  tmpassignment['status'] = '进行中'
                  break
                case 3:
                  tmpassignment['status'] = '已完成'
                  tmpassignment['score'] = assignment.score
                  break
                case 4:
                  tmpassignment['status'] = '纠纷中'
                  tmpassignment['score'] = assignment.score
                  break
                case 10:
                  tmpassignment['status'] = '试译中'
                  break
              }
              tmpassignment['price'] = assignment.price
              tmpassignment['submission'] = assignment.submission
              tmptask.assignments.push(tmpassignment)
            }
            that.tasklist.push(tmptask)
          }
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
    },
    mounted: function () {
      window.addEventListener('scroll', this.handleScroll)
    },
    destroyed: function () {
      window.removeEventListener('scroll', this.handleScroll)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin:20px 127px 10px 127px;
    padding: 0 16px 0 16px;
    width:1000px;
  }
  #left {
    padding: 3px;
    float:left;
    width: 700px;
  }
  #right {
    padding: 3px;
    width: 300px;
    margin-left: 703px;
  }
  #chosen {
    text-align: left;
  }
  #ads {
    margin:50px;
  }
  .order {
    font-size: 20px;
    font-weight: 700;
    width:20px;
    color: #495060;
    margin: 0 8px 0 5px;
  }
  .words {
    margin-right: 10px;
  }
  .chosen_by {
    margin: 10px 0 5px 0;
    color: #80848f;
  }
  .description {
    margin-left:28px;
  }
  .card {
    margin-bottom: 10px;
  }
  li {
    text-align: left;
    margin-top:5px;
    line-height: 200%;
  }
  h2 {
    color: #1c2438;
    text-align: left;
  }
  h3 {
    font-size: 16px;
    color: #495060;
    text-align: left;
  }
  h4 {
    font-size: 14px;
    font-weight: 400;
    color: #80848f;
    text-align: left;
  }
  p {
    font-size: 14px;
    color: #495060;
    text-align: left;
  }
  .isFixed {
    position: fixed;
    top: 0;
    z-index: 999;
  }
</style>
