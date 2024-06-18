<template>
  <el-card class="rounded-md dark:bg-black" shadow="hover">
    <div class="flex flex-items-center" v-waterMarker="{ text: 'dashboard', textColor: '#D9D9D9' }">
      <div class="p-l-20px">
        <div class="font-bold p-b-8px whitespace-nowrap">
          <span>数据大屏🌻</span>
          <div class="font-bold whitespace-nowrap">author: hcp🌻</div>
        </div>
        <!-- 搜索框 -->
        <el-input v-model="searchKeyWord" @keyup.enter="jumpToSearch" size="large" prefix-icon="Search">
          <template #suffix>
            <el-button type="primary" @click="jumpToSearch">搜索</el-button>
          </template>
        </el-input>
        <!-- 日期选择下拉框 -->
        <el-select v-model="selectedDate" @change="updateDate" placeholder="选择日期" class="p-t-8px">
          <el-option label="2024-05-27" value="2024-05-27"></el-option>
          <el-option label="更早" value="earlier"></el-option>
        </el-select>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const searchKeyWord = ref("");
const selectedDate = ref(store.state.selectedDate);
const router = useRouter();

function jumpToSearch() {
  router.push({ path: "/event/search", query: { keyword: searchKeyWord.value } });
}

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
  flex-direction: column;
  align-items: center;
  padding: 14px;
}
.flex .el-input {
  max-width: 500px;
}
.p-l-20px {
  padding-left: 20px;
}
.font-bold {
  font-weight: bold;
}
.p-b-8px {
  padding-bottom: 8px; /* Updated padding to 8px */
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
