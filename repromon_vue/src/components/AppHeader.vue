<template>
  <div class="header" style="display: flex; justify-content: space-between;">
    <div>
      <p>&nbsp;<b>ReproMon: </b>{{ screen_name }}</p>
    </div>
    <div>
      <p><b>Time:</b> {{ currentTime }} &nbsp;&nbsp;<b>User:</b> {{ currentUser.first_name }} {{ currentUser.last_name }}&nbsp;</p>
    </div>
  </div>
</template>

<script>
import '@/css/main.css'
import moment from 'moment';
import { LoginService } from '@/service/LoginService.js';
import {AppConfig} from "@/config";

export default {
  name: 'AppHeader',
  props: {
    screen_name: String,
    first_name: String,
    last_name: String
  },
  data() {
    return {
      currentTime: '',
      currentUser: {},
    };
  },
  mounted() {
    this.updateTime();
    setInterval(this.updateTime, 1000);
    this.getCurrentUser();
  },
  methods: {
    updateTime() {
      const now = moment().format('YYYY/MM/DD HH:mm:ss');
      this.currentTime = now;
    },
    async getCurrentUser() {
      try {
        this.currentUser = await LoginService.getCurrentUser();
        AppConfig.CURRENT_USER = this.currentUser
        console.log("set AppConfig.CURRENT_USER="+JSON.stringify(AppConfig.CURRENT_USER))
      } catch (error) {
        console.error('Failed to get current user:', error);
      }
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header {
  color: white;
  background-color: navy;
}
</style>
