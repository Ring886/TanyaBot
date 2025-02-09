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

  const response = ref('')
  const props = defineProps({
    message: String
  })

  async function quickChat(message) {
    console.log('message:', message)
    try {
      const res = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });

      if (!res.ok) {
        throw new Error('网络响应不正常');
      }

      const data = await res.json();
      console.log(data)
      response.value = data.response; // 更新响应内容
      console.log(data.response);
    } catch (error) {
      console.error('调用接口失败:', error);
      response.value = '调用失败，请检查控制台日志。';
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
