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