<template>
  <el-card class="rounded-md dark:bg-black" shadow="hover">
    <div class="flex flex-items-center" v-waterMarker="{ text: 'dashboard', textColor: '#D9D9D9' }">
      <div class="p-l-20px">
        <div class="font-bold p-b-8px whitespace-nowrap">
          <span>🌻数据大屏🌻</span>
        </div>
        <!-- 添加下拉框 -->
        <el-select v-model="selectedDate" @change="updateDate" placeholder="选择日期" class="p-t-8px">
          <el-option label="一个月" value="one-month"></el-option>
          <el-option label="更早" value="earlier"></el-option>
        </el-select>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, watch } from "vue";
import { useStore } from "vuex";

const store = useStore();
const selectedDate = ref(store.state.selectedDate);

const updateDate = value => {
  store.dispatch("updateSelectedDate", value);
};

// Watch for changes in Vuex state to update local ref
watch(
  () => store.state.selectedDate,
  newDate => {
    selectedDate.value = newDate;
  },
  { immediate: true }
);
</script>

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
.p-t-8px {
  padding-top: 8px;
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
  font-size: 22px;
  color: #007bff;
  vertical-align: middle;
}
</style>
