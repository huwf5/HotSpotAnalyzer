<template>
  <el-icon :size="$props.size" :color="$props.color" @click="click" :class="{ 'is-loading': loading }">
    <slot />
  </el-icon>
</template>

<script setup lang="ts">
defineProps({
  size: {
    type: Number,
    default: 15,
    required: false
  },
  color: {
    type: String,
    required: false
  },
  loading: {
    type: Boolean,
    default: false,
    required: false
  }
});
const emits = defineEmits(["click"]);
function click() {
  emits("click");
}
</script>
