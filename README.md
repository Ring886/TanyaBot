# 0.1 提交于2025/2/7
- 完善聊天界面,实现输入框和模拟了一下Bot与用户的聊天界面
- 待完善创建Python后端对接大模型接口实现回复

# 0.2 提交于2025/2/9
- 页面平滑滚动到底部:
  PS: 滚动的元素要带`overflow-auto`,否则加在`chatContainer`上无法滚动
  ``` vue
    <main class="overflow-auto h-screen" ref="mainContainer"></main>
    <div class="flex flex-col chat" ref="chatContainer">
      <BotSaying class="self-start"/>
    </div>
  ```
  ``` javascript
  nextTick(() => {
    scrollToBottom()
  })
  const scrollToBottom = () => {
    nextTick(() => { // 确保 DOM 更新完成
      console.log(mainContainer.value.scrollHeight)
      if (chatContainer.value) {
        mainContainer.value.scrollTo({
          top: mainContainer.value.scrollHeight,
          behavior: 'smooth',
        })
      }
    })
  }
  ```
- 使聊天区域距离输入框始终保持距离
  1. `chatContainer` 设置 `margin-bottom`
  2. `inputContainer` 设置绝对定位, `bottom:0`
- 实现简单的发送并回复
- 待实现
  1. `流式回复`,减少用户等待时间
  2. 智能取左侧栏标题名字
  3. 将聊天记录存储起来,实现持久化存储,目前刷新就消失
  4. 保留记忆


# 0.3 提交于2025/2/11
- 实现终端流式回复,目前界面的流式回复还无法实现


# 0.4 提交于2025/2/15
- 在`Mac`上跑项目时遇到了`cors`问题,上网找了很多解决办法,无济于事,控制台报错的位置显示`await fetch()`这一句出了问题,然后又去postman上测试,本抱着试一试的心态,把`fetch`的`url`从`http://localhost:5000/api/chat`改成`http://127.0.0.1:5000/api/chat`,没想到真的出来了,我是真不知道原理是什么,在`Windows`上`localhost`就可以
- 还有个问题
  ``` python
  # 原写法
  @app.route('/api/chat', methods=['POST'])
  # 照网上和chat改后
  @app.route('/api/chat', methods=['POST', 'OPTION'])
  ```
  经过实践,这纯粹扯犊子,由于没有系统学习过`python`,所以不知道原理,但是通过`devtools`发现如果加了`OPTION`,发送请求会出现`415错误`,而且是针对`OPTION`的,具体为`媒体类型错误`我记得.
- 这段时间就是在改`Mac`上的报错,以便后续项目的进行





# 0.5 提交于2025/2/16
- 实现打字机式回复,是在后端修改了
  ``` python
  if chunk:
    yield f"{chunk}"  # **用 yield 返回数据**
  ```
  然后前端直接
  ``` javascript
  response.value += chunk
  ``` 
- 解决了换行问题,具体看`BotSaying`组件
  `style`实现前端界面换行(遇到\n,读取转义字符)
  ``` vue
  <p class="chatbox" style="white-space: pre-wrap;">{{ response }}</p>
  ```
- 待完善
  1. AI回复时保持滚动条始终在底部
  2. 发送消息防抖
  3. 聊天记录储存