<template>
    <div class = "switcher">
      <transition appear mode="out-in" name="switching"
        leave-active-class="animate__animated animate__zoomOut"
        enter-active-class="animate__animated animate__fadeIn"

      >
          <CreateCourse v-if="currentStep === 'create-course'" @courseCreated="handleCourseCreated" />
          <UploadMaterial v-else-if="currentStep === 'upload-material'" :courseId="courseId" @materialUploaded="handleMaterialUploaded" />
          <Waiting v-else-if="currentStep === 'waiting'" />
      </transition>
    </div>

</template>

<script>
import CreateCourse from './CreateCourse.vue';
import UploadMaterial from './UploadMaterial.vue';
import Waiting from './Waiting.vue';
import 'animate.css';

export default {
  components: {
    CreateCourse,
    UploadMaterial,
    Waiting
  },
  data() {
    return {
      currentStep: 'create-course',
      courseId: null
    };
  },
  methods: {
    handleCourseCreated(courseId) {
      this.courseId = courseId;
      this.currentStep = 'upload-material';
    },
    handleMaterialUploaded() {
      this.currentStep = 'waiting';
    }
  }
};
</script>

<style scoped>
.switcher{
    overflow: hidden;
}
</style>
