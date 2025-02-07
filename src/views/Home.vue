<template>
  <div class="flex">
    <!-- 左侧栏：导航栏或菜单 -->

    <Aside @itemSelected="handleItemSelected" @BarWidth="BarWidth"/>
    
    <Setting :isOpen="isSidebarOpen" :width="width"/>


    <!-- 右侧栏：主要内容区域 -->
    <main class="flex-1 bg-gray-100 overflow-auto relative h-screen" >
      <header class="text-xl py-2 px-5 h-12">
        <a @click="toggleSidebar" class="text-2xl absolute left-4 cursor-pointer hover:bg-gray-300">📑</a>
        <a @click="newText" class="text-2xl absolute cursor-pointer right-5 hover:bg-gray-300 ">📝</a>
      </header>
      <hr class="mx-5 border-gray-300">
      

      <div class="flex flex-col chat">
        <BotSaying class="self-start"/>
        <UserSaying class="self-end"/>
        <BotSaying class="self-start"/>
        <UserSaying class="self-end"/>
      </div>

      <!-- <div v-if="selectedItem" class="p-5" :style="`height: ${innerHeight - 100}px;`">
        <h2 class="text-2xl font-bold">
          <input v-model="selectedItem.title" type="text"
            class="w-full bg-transparent border-b-2 border-gray-300 p-1 text-2xl font-bold outline-none" ref="TitleGetFocus"/>
        </h2>
        <textarea v-model="selectedItem.text" class="text-lg bg-transparent border-b-2 border-gray-300 p-1 text-lg outline-none w-full h-full"  
      @input="changeText" ref="TextGetFocus"></textarea>
      </div> -->


      <!-- <hr class="m-5 border-gray-300"> -->
      <!-- <div class="h-80 bg-red-200 m-4 rounded-xl"></div> -->
      <div class="p-3 flex items-center input">
        <textarea
          type="text"
          class="flex-1 p-2 h-12 rounded-xl border-gray-500 shadow-lg 
            focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="输入消息..."></textarea>
        <button class="ml-3 bg-blue-500 text-white p-2 rounded-full">
          🚀
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
  import { ref, onUnmounted, watch } from 'vue'
  import { useMemoStore } from '../store/index'
  import Aside from "../components/Aside.vue"
  import Setting from "../components/Setting.vue"
  import BotSaying from '@/components/BotSaying.vue'
  import UserSaying from '@/components/UserSaying.vue'

  const innerHeight = ref(window.innerHeight)
  window.addEventListener('resize', () => {
    innerHeight.value = window.innerHeight
  })

  // 引入 Pinia store
  const memoStore = useMemoStore()

  // 控制侧边栏的展开与收起
  const isSidebarOpen = ref(false)

  // Aside 子组件通信
  // const selectedItem = ref(null)
  const selectedItem = ref(memoStore.memos[0])

  // 切换侧边栏的状态
  const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value
  }

  // 处理从 Aside 传递过来的选中项
  const handleItemSelected = (item) => {
    selectedItem.value = item
    // console.log(selectedItem.value.text)
  }

  const width = ref(200)
  const BarWidth = (item) => {
    width.value = item
  }

  // 失去焦点后更新数据
  const changeText = () => {
    if (selectedItem.value) {
      // 使用 Pinia 的 updateMemo 方法更新备忘录
      memoStore.updateMemo(selectedItem.value.id, selectedItem.value.title, selectedItem.value.text)
      // console.log(selectedItem.value.id)
    }
  }


  const TitleGetFocus = ref(null);
  const TextGetFocus = ref(null);

  const newText = () => {
    memoStore.addMemo('未命名标题', '')
    selectedItem.value = memoStore.memos[0]
    console.log(memoStore.memos[0])
    console.log(selectedItem.value)
    if(TitleGetFocus.value) {
      TitleGetFocus.value.focus()
    }
  }

  onUnmounted(() => {
    // console.log('hhh')
    changeText()
  })
  watch(selectedItem, (newValue, oldValue) => {
    console.log('oldValue:', oldValue)
    // console.log(111)
    console.log(newValue.title)
    if(oldValue) {
      if(TitleGetFocus.value || newValue.id !== oldValue.id) {
        if(newValue.text) {
          TextGetFocus.value.focus()
        } else {
          TitleGetFocus.value.focus()
        }
      }
    }
  }, {deep:true})


</script>

<style scoped>
  header {
    -webkit-app-region: drag;
    /* position: absolute;
    top: 0; */
  }
  .aside {
    max-width: 100%;
    /* width: auto; */
  }

  .chat {
    margin-bottom: 10px;
  }

  /* input {
    height: 100px;
  } */
  /* input::-webkit-input-placeholder {
    position: relative;
    top: -1.7em;
  } */
  textarea {
    resize: none;
    height: 85px;
  }
  .input {
    position: sticky;
    bottom: 0;
  }
  ::-webkit-scrollbar{width:8px;height:4px;}
  ::-webkit-scrollbar-button{width:8px;height:0}
  ::-webkit-scrollbar-track{background:0 0; margin-top: 10px;margin-bottom: 10px;}
  ::-webkit-scrollbar-thumb{background:#8e9194;-webkit-transition:.3s;transition:.3s;border-radius: 5px;}
  ::-webkit-scrollbar-thumb:hover{background-color:#646769}
  ::-webkit-scrollbar-thumb:active{background-color:#555758}
</style>