<template>
  <div class="message-log-view">
    <table style="width: 100%; padding: 0px; margin: 0px; padding-bottom: 4px;">
      <tr>
        <td style="text-align: left;">
          <b style="color: red;">Errors:</b> {{ errorCount }},
          <b>Warnings:</b> {{ warnCount }}
          <button @click="resetMessages()">Reset</button>
        </td>
        <td style="text-align: right; padding: 0px; margin: 0px;" >
          <div style="display: flex; justify-content: flex-end; padding: 0px; margin: 0px;">
            <button @click="clearMessages('*')">Clear All</button>&nbsp;
            <button @click="clearMessages('ERROR')">Clear ERROR</button>&nbsp;
            <button @click="clearMessages('WARN')">Clear WARN</button>&nbsp;
            <button @click="clearMessages('INFO')">Clear INFO</button>&nbsp;
            <button @click="reload()">Reload</button>
          </div>
        </td>
      </tr>
    </table>

    <div class="data-grid">
      <div class="header-row">
        <div class="column" style="width: 30px;">#</div>
        <div class="column" style="width: 110px;">Date</div>
        <div class="column" style="width: 90px;">Time</div>
        <div class="column" style="width: 70px;">Level</div>
        <div class="column" style="width: 120px;">Provider</div>
        <div class="column"  style="width: 1000px;">Description</div>
      </div>

      <div class="body-rows">
        <div
            v-for="(item, index) in messageLog"
            :key="item.id"
            class="row"
            :class="{ 'selected-row': selectedItemId === item.id }"
            @click="selectRow(item.id)"
        >
          <div class="column" style="width: 30px;"> {{ index + 1 }}</div>
          <div class="column" style="width: 110px;">{{ formatDate(item.ts) }}</div>
          <div class="column" style="width: 90px;">{{ formatTime(item.ts) }}</div>
          <div class="column" style="width: 70px;" :style="{ color: item.level === 'ERROR' ? 'red' : 'inherit' }">{{ item.level }}</div>
          <div class="column" style="width: 120px;">{{ item.provider }}</div>
          <div class="column flex-column" style="width: 1000px;">{{ item.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import moment from 'moment';
import {AppConfig} from '@/config.js'
import { FeedbackService } from '@/service/FeedbackService.js';

export default {
  props: {
    study_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      messageLog: [],
      selectedItemId: null,
    };
  },
  computed: {
    errorCount() {
      return ""+this.messageLog.filter(message => message.level === 'ERROR').length;
    },
    warnCount() {
      return ""+this.messageLog.filter(message => message.level === 'WARN').length;
    },
  },
  mounted() {
    this.fetchMessageLog();
    this.socket = new WebSocket(`${AppConfig.WS_BASE_URL}/ws`);
    this.socket.onmessage = (event) => {
      console.log("onmessage: data="+event.data)
      var msg = JSON.parse(event.data)
      console.log("topic="+msg.topic)
      if( msg.topic=="feedback-log-refresh" && msg.body.study_id==this.study_id )
        this.reload()
      if( msg.topic=="feedback-log-add" && msg.body.study_id==this.study_id )
        this.addMessage(msg.body.message_id)
    };
    this.socket.onopen = function(event) {
      console.log("onopen: "+event)
    }
  },
  methods: {
    async addMessage(message_id) {
      console.log("addMessage(message_id="+message_id+")")
      var msg = await FeedbackService.getMessage(message_id);
      this.messageLog.push(msg)
      this.$forceUpdate();
    },
    async clearMessages(mask) {
      //this.messageLog = this.messageLog.filter(message => (message.level !== mask && mask != '*' ));
      await FeedbackService.setMessageLogVisibility(this.study_id, false, mask);
      //this.reload() <-- will be sent via websocket
      //alert('Clear: '+mask);
    },
    async fetchMessageLog() {
      console.log("fetchMessageLog")
      try {
        this.messageLog = await FeedbackService.getMessageLog(this.study_id);
      } catch (error) {
        console.error('Failed to fetch message log:', error);
      }
    },
    formatDate(timestamp) {
      return moment(timestamp).format('YYYY-MM-DD');
    },
    formatTime(timestamp) {
      return moment(timestamp).format('HH:mm:ss');
    },
    reload() {
      console.log("reload")
      this.fetchMessageLog()
    },
    async resetMessages() {
      console.log("resetMessages")
      await FeedbackService.setMessageLogVisibility(this.study_id, true, '*');
      //this.reload() <-- will be sent via websocket
    },
    selectRow(itemId) {
      this.selectedItemId = itemId;
    },
  },
};
</script>

<style>
.message-log-view {
  /* Component styles */
  padding: 13px;
}

.data-grid {
  /* max-height: 300px; */
  overflow-y: auto;
  border: 1px solid #ccc;
}

.header-row {
  display: flex;
  /*grid-template-columns: repeat(6, 60px) 1fr;*/
  background-color: #f0f0f0;
  font-weight: bold;
  padding: 8px;
}

.row {
  display: flex;
  /*grid-template-columns: repeat(6, 60px) 1fr;*/
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}

.row:hover {
  background-color: #f0f0f0;
}

.row.selected-row {
  background-color: #e0e0e0;
}

.column {
  /*flex: 1;*/
  padding: 2px;
  /*border-right: 1px solid #ccc;*/
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.column-fixed-width {
  width: 60px;
}

.flex-column {
  flex: auto;
  min-width: 0;
  white-space: normal;
  word-wrap: break-word;
}
</style>
