<template>
  <el-dialog v-model="visible" title="上传头像">
    <el-upload drag accept="image/*">
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">将图片拖至此处或 <em>点击上传</em></div>
      <template #tip>
        <div class="el-upload__tip">图片大小不超过2MB</div>
      </template>
    </el-upload>
  </el-dialog>
</template>

<script setup lang="ts">
const visible = defineModel<boolean>();
</script>
