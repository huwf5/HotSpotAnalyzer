<template>
  <el-card class="rounded-md dark:bg-black" shadow="hover">
    <div class="flex flex-items-center" v-waterMarker="{ text: 'dashboard', textColor: '#D9D9D9' }">
      <div class="p-l-20px">
        <div class="font-bold p-b-8px whitespace-nowrap">
          <span>事件图谱</span>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup></script>

<style scoped>
.rounded-md {
  border-radius: 8px;
  box-shadow: 0 4px 6px rgb(0 0 0 / 10%);
}
.dark\:bg-black {
  background-color: #ffffff;
}
.flex {
  display: flex;
  align-items: center;
  padding: 16px;
}
.p-l-20px {
  padding-left: 20px;
}
.font-bold {
  font-weight: bold;
}
.p-b-8px {
  padding-bottom: 10px;
}
.whitespace-nowrap {
  white-space: nowrap;
}
.el-card[shadow="hover"]:hover {
  box-shadow: 0 8px 16px rgb(0 0 0 / 20%);
}
.watermark {
  color: #d9d9d9;
}
span,
.font-bold div {
  font-size: 18px;
  color: #007bff;
  vertical-align: middle;
}
</style>
