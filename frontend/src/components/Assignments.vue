<template>
  <div class="root">
    <div id="assignments" class="card">
      <Card shadow class="assignments" padding=0>
        <div id="assignmentListTitle"><h2>我的任务</h2></div>
        <div id="bigCheckBox">
          <Row>
            <Col span="3"><div id="checkText"><h4>筛选：</h4></div></Col>
            <Col span="15">
              <div id="checkBox">
                <CheckboxGroup v-model="filter">
                  <Checkbox label="艺术"></Checkbox>
                  <Checkbox label="历史"></Checkbox>
                  <Checkbox label="文学"></Checkbox>
                </CheckboxGroup>
              </div>
            </Col>
            <Col span="5">
              <Select v-model="sort" placeholder="<排序方式>">
                <Option v-for="item in sortList" :value="item.value" :key="item.value">{{ item.label }}</Option>
              </Select>
            </Col>
          </Row>
        </div>
        <div>
          <ul>
            <li v-for="assignment in pageList">
              <Card padding=10 @click.native="checkAssignment(assignment.id)">
                <p slot="title" id="assignmentTitle">
                  {{ assignment.title }}&nbsp;&nbsp;&nbsp;<span v-for="tag in assignment.tags"><Tag><h4>{{ tag }}</h4></Tag></span>
                </p>
                <p id="assignmentTime">起始时间：{{ assignment.publishTime }}&nbsp;&nbsp;&nbsp;截止时间：{{ assignment.ddlTime }}</p>
                <p id="assignmentDescription">{{ assignment.description }}</p>
              </Card>
            </li>
          </ul>
        </div>
      </Card>
      <div id="pages">
        <Page :total="page_total_num" page-size="5" show-elevator @on-change="setPageList"></Page>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-new */
  export default {
    name: 'assignments',
    data () {
      return {
        filter: [],
        sort: '',
        page_total_num: 0,
        sortList: [
          {
            label: '按发布时间',
            value: 'publishTime'
          },
          {
            label: '按最后动态时间',
            value: 'changeTime'
          }
        ],
        assignmentlist: [
          {
            title: '',
            publishTime: '',
            ddlTime: '',
            tags: [],
            language: '',
            description: ''
          },
          {
            title: '',
            publishTime: '',
            ddlTime: '',
            tags: [],
            language: '',
            description: ''
          }
        ],
        pageList: []
      }
    },
    created: function () {
      const headers = new Headers({
        'Content-Type': 'application/json'
      })
      let that = this
      fetch('api/GetTranslatorAssignments', { method: 'GET',
        headers,
        credentials: 'include'})
      .then(function (response) {
        return response.json().then(function (data) {
          that.assignmentlist = []
          for (let assignment of data.assignmentList) {
            that.assignmentlist.push({
              id: assignment.id,
              title: assignment.title,
              publishTime: Date(assignment.publishTime),
              ddlTime: Date(assignment.ddlTime),
              tags: assignment.tag,
              language: assignment.language,
              description: assignment.description
            })
          }
          that.page_total_num = that.assignmentlist.length
          that.setPageList(1)
        })
      }).catch(function (ex) {
        alert('Network Error')
      })
    },
    methods: {
      checkAssignment (assignmentid) {
        this.$router.push('/assignment/' + assignmentid)
      },
      setPageList (page) {
        this.pageList.splice(0, this.pageList.length)
        this.pageList = this.assignmentlist.slice((page - 1) * 5, page * 5)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .root {
    margin-left: 460px;
    width: 600px;
    padding: 20px;
  }
  .card {
    margin-bottom: 20px;
  }
  #checkText {
    margin-top: 3px;
  }
  #checkBox {
    float: left;
    margin-bottom: 15px;
  }
  #bigCheckBox {
    height: 20px;
    margin-top: 10px;
    margin-bottom: 20px;
  }
  #assignmentListTitle {
    text-align: left;
    padding: 20px 0 10px 20px;
  }
  #assignmentTitle {
    font-size: 16px;
    text-align: left;
  }
  #assignmentDescription {
    text-align: left;
    color: #495060;
  }
  #assignmentTime {
    font-size: 12px;
    text-align: left;
    color: #80848f;
  }
  #pages {
    padding: 20px;
  }
  h2 {
    font-size: 20px;
    color: #1c2438;
  }
  h4 {
    font-size: 12px;
  }
</style>
