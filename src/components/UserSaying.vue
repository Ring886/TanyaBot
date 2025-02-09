<template>
  <div class="p-4 flex">
    <!-- <div class="chatbox">
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      风水轮流转,悲喜各一半<br>
      这是今天的第六遍
    </div> -->
    <p class="chatbox">{{ message }}</p>

    <div class="w-8 h-8 rounded-full overflow-hidden flex-none">
      <img src="../../src/assets/1.jpg" alt="Icon" class="w-full h-full object-cover" />
    </div>


  </div>


</template>


<script setup>
  import { defineProps, onMounted } from 'vue'
  const props = defineProps({
    message: String
  })
  onMounted(() => {
    // console.log(props.message)
  })
</script>


<style scoped>
  .chatbox {
    margin-right: 12px;
    padding: 5px;
    max-width: 16rem;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(95, 93, 93, 0.2); /* 阴影 */
  }
</style>
