<template>
  <el-card class="rounded-md dark:bg-black" shadow="hover">
    <div class="flex flex-items-center" v-waterMarker="{ text: 'dashboard', textColor: '#D9D9D9' }">
      <div class="p-l-20px">
        <div class="font-bold p-b-8px whitespace-nowrap">
          <span>数据大屏🌻</span>
          <div class="font-bold whitespace-nowrap">author: hcp🌻</div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup></script>

<style scoped>
.rounded-md {
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dark\:bg-black {
  background-color: #ffffff;
}

.flex {
  display: flex;
  align-items: center;
  padding: 14px;
}

.p-l-20px {
  padding-left: 20px;
}

.font-bold {
  font-weight: bold;
}

.p-b-8px {
  padding-bottom: 24px;
}

.whitespace-nowrap {
  white-space: nowrap;
}

.el-card[shadow="hover"]:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.watermark {
  color: #d9d9d9;
}

span,
.font-bold div {
  vertical-align: middle;
  color: #007bff;
  font-size: 22px;
}
</style>