<template>
  <div id="root">
    <div id="left">
      <Menu :theme="theme" active-name="1">
        <MenuGroup title="申诉管理">
          <MenuItem name="1">
            <Icon type="document-text"></Icon>
            尚未处理
          </MenuItem>
          <MenuItem name="2">
            <Icon type="document-text"></Icon>
            已经处理
          </MenuItem>
        </MenuGroup>
        <MenuGroup title="证书审核">
          <MenuItem name="3">
            <Icon type="document-text"></Icon>
            尚未处理
          </MenuItem>
          <MenuItem name="4">
            <Icon type="document-text"></Icon>
            已经处理
          </MenuItem>
        </MenuGroup>
      </Menu>
    </div>
    <div id="right">
      <ul>
        <li v-for="a in argues">
          <div class="card">
            <Card dis-hover>
              <p>翻译者：{{ a.argument_translator }}</p>
              <p>雇主：{{ a.argument_employer }}</p>
              <div v-if="a.status == '未审核'" class="buttons">
                <Button type="primary">同意</Button>
                <Button type="error">不同意</Button>
                <div class="input">
                  <Input v-model="a.reason" type="textarea" size="large"></Input>
                </div>
              </div>
            </Card>
          </div>
        </li>
      </ul>
      <div class="center"><Page :total="100" show-elevator></Page></div>
    </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        theme: 'light',
        argues: [
          {
            status: '已审核',
            assignment_name: 'name',
            argument_translator: '我觉得翻译很差不能给这么多钱',
            argument_employer: '我觉得没问题',
            result: '',
            reason: ''
          },
          {
            status: '未审核',
            assignment_name: 'name',
            argument_translator: '我觉得翻译很差不能给这么多钱',
            argument_employer: '我觉得没问题',
            result: '',
            reason: ''
          }
        ]
      }
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
