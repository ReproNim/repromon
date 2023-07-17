<template>
  <table style="padding: 10px;">
    <tr>
      <td><b>Status:</b></td>
      <td>{{ studyHeader.status }}</td>
    </tr>
    <tr>
      <td><b>Study:</b></td>
      <td>{{ studyHeader.study }}</td>
    </tr>
    <tr>
      <td><b>Device:</b></td>
      <td>{{ studyHeader.device }}</td>
    </tr>
  </table>
</template>

<script>
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
      studyHeader: {},
    };
  },
  mounted() {
    this.getStudyHeader();
  },
  methods: {
    async getStudyHeader() {
      console.log("getStudyHeader")
      try {
        this.studyHeader = await FeedbackService.getStudyHeader(this.study_id); // Replace 123 with the actual study ID
      } catch (error) {
        console.error('Failed to get study header:', error);
      }
    },
  },
};
</script>
