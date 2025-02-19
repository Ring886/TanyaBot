<template>
  <div class="flex flex-col p-4 ">
    <div class="flex">
      <div class="w-8 h-8 rounded-full overflow-hidden flex-none">
        <img src="../../src/assets/2.jpg" alt="Icon" class="w-full h-full object-cover" />
      </div>
      <p class="chatbox" style="white-space: pre-wrap;">{{ response }}</p>
      <!-- white-space: pre-wrap;很关键 -->
    </div>
    <div class="flex group">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-md ml-12 mt-2 refresh  text-gray-500 hover:text-gray-700">
        <path d="M3.06957 10.8763C3.62331 6.43564 7.40967 3 12 3C14.2824 3 16.4028 3.85067 18.0118 5.25439V4C18.0118 3.44772 18.4595 3 19.0118 3C19.5641 3 20.0118 3.44772 20.0118 4V8C20.0118 8.55228 19.5641 9 19.0118 9H15C14.4477 9 14 8.55228 14 8C14 7.44772 14.4477 7 15 7H16.9571C15.6757 5.76379 13.9101 5 12 5C8.43108 5 5.48466 7.67174 5.0542 11.1237C4.98586 11.6718 4.48619 12.0607 3.93815 11.9923C3.39011 11.924 3.00123 11.4243 3.06957 10.8763ZM20.0618 12.0077C20.6099 12.076 20.9988 12.5757 20.9304 13.1237C20.3767 17.5644 16.5903 21 12 21C9.72322 21 7.60762 20.1535 5.99999 18.7559V20C5.99999 20.5523 5.55228 21 4.99999 21C4.44771 21 3.99999 20.5523 3.99999 20V16C3.99999 15.4477 4.44771 15 4.99999 15H8.99999C9.55228 15 9.99999 15.4477 9.99999 16C9.99999 16.5523 9.55228 17 8.99999 17H7.04285C8.32433 18.2362 10.0899 19 12 19C15.5689 19 18.5153 16.3283 18.9458 12.8763C19.0141 12.3282 19.5138 11.9393 20.0618 12.0077Z" fill="currentColor"></path>
      </svg>
      <div class="relative top-5 transform -translate-x-3 mt-2 hidden group-hover:block bg-black text-white text-xs rounded p-2" style="will-change: auto; overflow:hidden;">
        重新发送
      </div>
    </div>
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

      response.value = ''
      // 读取流式响应
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let accumulatedText = "";

      while (true) {
        // console.log('1')
        const { done, value } = await reader.read();
        // console.log('2')
        if (done) break;
        // console.log('3')
        let chunk = decoder.decode(value, { stream: true }); // 解码当前数据块
        accumulatedText += chunk; // 累积文本
        // console.log('4')
        console.log("流式数据:", JSON.stringify(chunk));
        response.value += chunk
        
        // response.value += chunk.replace(/\\n/g, '\n'); // 处理转义的 \n

        // 处理 OpenAI API 流式响应（data: JSON 格式）
        // const lines = accumulatedText.split("\n"); // 按行分割
        // accumulatedText = lines.pop(); // 可能是不完整的 JSON，暂存等待下一批数据

        // for (let line of lines) {
        //   console.log('进入循环')
        //   // if (line.startsWith("data: ")) {
        //   //   try {
        //   //     let json = JSON.parse(line.substring(6)); // 解析 JSON
        //   //     let textChunk = json.choices[0].delta.content || "";
        //   //     response.value += textChunk; // 更新 UI 响应内容
        //   //   } catch (error) {
        //   //     console.error("JSON 解析失败:", error);
        //   //   }
        //   // }
        //   try {
        //     // console.log(typeof line)
        //     // let json = JSON.parse(line); // 解析 JSON
        //     // console.log("json:", json)
        //     // let textChunk = json.choices[0].delta.content || "";
        //     response.value += line; // 更新 UI 响应内容
        //   } catch (error) {
        //     console.error("JSON 解析失败:", error);
        //   }
        // }
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
    max-width: 32rem;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(95, 93, 93, 0.2); /* 阴影 */
  }
  .icon-md {
    stroke-width: 1.5;
    flex-shrink: 0;
  }
  .refresh {
    stroke-width: 1.5;
    flex-shrink: 0;

  }

</style>
