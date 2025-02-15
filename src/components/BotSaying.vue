<template>
  <div class="p-4 flex">
    <div class="w-8 h-8 rounded-full overflow-hidden flex-none">
      <img src="../../src/assets/2.jpg" alt="Icon" class="w-full h-full object-cover" />
    </div>

    <!-- <p class="chatbox">
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      这是今天的第六遍
    </p> -->
    <p class="chatbox">{{ response }}</p>
  </div>


</template>


<script setup>
  import { ref, defineProps, onMounted } from 'vue'

  const response = ref('…')
  const props = defineProps({
    message: String
  })

  async function quickChat(message) {
    console.log('message:', message);
    try {
      const res = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });

      if (!res.ok) {
        throw new Error('网络响应不正常');
      }

      // 读取流式响应
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let accumulatedText = "";

      while (true) {
        console.log('1')
        const { done, value } = await reader.read();
        console.log('2')
        if (done) break;
        console.log('3')
        let chunk = decoder.decode(value, { stream: true }); // 解码当前数据块
        accumulatedText += chunk; // 累积文本
        console.log('4')
        console.log("流式数据:", chunk);

        // 处理 OpenAI API 流式响应（data: JSON 格式）
        const lines = accumulatedText.split("\n"); // 按行分割
        accumulatedText = lines.pop(); // 可能是不完整的 JSON，暂存等待下一批数据

        for (let line of lines) {
          console.log('进入循环')
          if (line.startsWith("data: ")) {
            try {
              let json = JSON.parse(line.substring(6)); // 解析 JSON
              let textChunk = json.choices[0].delta.content || "";
              response.value += textChunk; // 更新 UI 响应内容
            } catch (error) {
              console.error("JSON 解析失败:", error);
            }
          }
        }
      }

      console.log("流式响应完成");
    } catch (error) {
      console.error("调用接口失败:", error);
      response.value = "调用失败，请检查控制台日志。";
    }
  }


  onMounted(() => {
    quickChat(props.message)
    console.log('props.message:', props.message)
  })

</script>


<style scoped>
  .chatbox {
    margin-left: 12px;
    padding: 5px;
    max-width: 16rem;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(95, 93, 93, 0.2); /* 阴影 */
  }
</style>
