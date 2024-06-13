<template>
  <div class="content">
    <h1>{{ msg = "Home page ~" }}</h1>

    <p>
      <a href="https://vitejs.dev/guide/features.html" target="_blank" class="btn-link">Vite Doc</a>
      |
      <a href="https://v3.vuejs.org/" target="_blank" class="btn-link">Vue 3 Doc</a>
    </p>

    <button @click="state.count++" class="btn custom-count-btn">count is: {{ state.count }}</button>
    <p>{{ data.text1 }}</p>
    <p>{{ data.text2 }}</p>
  </div>
  <!-- <p> Edit <code>components/HelloWorld.vue</code> to test hot module replacement.</p> -->

</template>

<script setup>
import {defineProps, onMounted, reactive} from 'vue'
import axios from 'axios'

defineProps({
  msg: String
})


const state = reactive({ count: 0 })
const data = reactive({ text1: "" })

onMounted(async () => {
  try {
    const response1 = await axios.get('http://127.0.0.1:8010/hello')
    data.text1 = response1.data

    const response2 = await axios.post('http://127.0.0.1:8010/hello')
    data.text2 = response2.data
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})
</script>

<style scoped>
h1{
    margin-top: 3rem;
}
a, p {
  font-size: 120%;
  color: wheat;
  margin: 1rem; /* 调整段落的底部外边距以控制行间距 */
}

.custom-count-btn {
  margin-bottom: 10px; /* 间距 */
  background-color: powderblue; /* 按钮背景色 */
  color: darkblue; /* 按钮文字色 */
}



</style>
