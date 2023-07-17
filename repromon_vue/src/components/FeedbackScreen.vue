<template>
  <StudyHeader :study_id="study_id"/>
  <MessageLogView :study_id="study_id"/>
</template>

<script>
import MessageLogView from '@/components/MessageLogView.vue';
import StudyHeader from '@/components/StudyHeader.vue';

export default {
  props: {
    study_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
    };
  },
  mounted() {
    console.log("mounted")
    this.reload();
  },
  methods: {
    async reload() {
        console.log("reload")
    },
  },
  components: {
    MessageLogView,
    StudyHeader
  }
};
</script>
