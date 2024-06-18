<template>
  <el-row :gutter="20" class="m-t-5px">
    <!-- 注意：如果不进行操作数组，使用index当key没有问题，若是数组会用来增删改查则不能使用index当key。 -->
    <el-col :span="6" :lg="6" :md="12" :sm="12" :xs="24" v-for="(item, index) in cardList" :key="index + new Date().getTime()">
      <el-card class="rounded-md dark:bg-black" shadow="hover">
        <div class="flex justify-between">
          <span class="text-sm">{{ item.title1 }}</span>
          <el-tag :type="index == 0 ? 'primary' : index == 1 ? 'success' : index == 2 ? 'warning' : 'danger'">{{
            item.unit
          }}</el-tag>
        </div>
        <div class="text-2xl"><CountTo :start-val="0" :end-val="item.value1" :duration="2000"></CountTo></div>
        <el-divider direction="horizontal" content-position="left"></el-divider>
        <div class="flex justify-between">
          <span class="text-sm">{{ item.title2 }}</span>
          <span><CountTo :start-val="0" :end-val="item.value2" :duration="2000"></CountTo></span>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { CountTo } from "vue3-count-to";
import { reactive } from "vue";

const response = await fetch("http://127.0.0.1:8000/fetch-cardList");
const message = await response.json();

const cardList = reactive([
  {
    title1: "上月帖子数量",
    unit: "月",
    value1: message["last_month"]["posts"],
    title2: "总帖子数量",
    value2: message["history"]["posts"]
  },
  {
    title1: "上月点赞数",
    unit: "月",
    value1: message["last_month"]["like_counts"],
    title2: "总点赞数",
    value2: message["history"]["like_counts"]
  },
  {
    title1: "上月讨论量",
    unit: "月",
    value1: message["last_month"]["comment_counts"],
    title2: "总讨论量",
    value2: message["history"]["comment_counts"]
  },
  {
    title1: "上月转发数",
    unit: "月",
    value1: message["last_month"]["forward_counts"],
    title2: "总转发数",
    value2: message["history"]["forward_counts"]
  }
]);
</script>

<style lang="scss" scoped>
.el-card {
  background-color: #ffffff;
  border-radius: 8px;
  transition: box-shadow 0.3s;
}
.el-card:hover {
  box-shadow: 0 4px 20px rgb(0 0 0 / 10%);
}
.el-tag {
  font-size: 12px;
}
.flex {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.text-sm {
  font-size: 14px;
}
.text-2xl {
  font-size: 24px;
  font-weight: bold;
}
.m-t-5px {
  margin-top: 5px;
}
</style>
