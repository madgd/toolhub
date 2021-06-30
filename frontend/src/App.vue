<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <n-message-provider>
<!--  <HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <Home/>
  </n-message-provider>

</template>

<script>
import { NMessageProvider } from 'naive-ui';
// import HelloWorld from './components/HelloWorld.vue'
import Home from './components/Home.vue'
// import defineComponent from './components/Home.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld
    NMessageProvider,
    Home
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
