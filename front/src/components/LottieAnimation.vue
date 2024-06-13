<template>
  <div ref="lottieContainer" class="lottie-container"></div>
</template>

<script>
import lottie from 'lottie-web';

export default {
  props: {
    animationPath: {
      type: String,
      required: true
    },
    loop: {
      type: Boolean,
      default: true
    },
    autoplay: {
      type: Boolean,
      default: true
    }
  },
  mounted() {
    this.loadAnimation();
  },
  methods: {
    loadAnimation() {
      lottie.loadAnimation({
        container: this.$refs.lottieContainer,
        renderer: 'svg',
        loop: this.loop,
        autoplay: this.autoplay,
        path: this.animationPath
      });
    }
  }
};
</script>

<style scoped>
.lottie-container {
  width: 100px; /* Adjust the size as needed */
  height: 100px; /* Adjust the size as needed */
  margin: 0 auto;
}
</style>
