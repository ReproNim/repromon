<template>
  <AppHeader screen_name="Feedback Screen" first_name="?" last_name="?"/>
  <FeedbackScreen :study_id="1"/>
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import FeedbackScreen from "@/components/FeedbackScreen.vue";

export default {
  name: 'App',
  components: {
    AppHeader,
    FeedbackScreen,
  }
}
</script>

<style>
html, body {
  margin:0;
  padding:0;
  height:100%;
}
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  */

  margin: 0px;
  padding: 0px;
}
</style>
