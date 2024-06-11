<template>
  <div class="p-6px">
    <DashBoardTitle></DashBoardTitle>
    <BasicInfoCard></BasicInfoCard>
    <el-row :gutter="20" class="m-t-5px">
      <el-col :span="12" :lg="12" :md="12" :sm="24" :xs="24">
        <el-card class="rounded-md dark:bg-black" shadow="hover">
          <WordCloudChart></WordCloudChart>
        </el-card>
      </el-col>
      <el-col :span="12" :lg="12" :md="12" :sm="24" :xs="24">
        <el-card class="rounded-md dark:bg-black" shadow="hover">
          <EmotionChart></EmotionChart>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="m-t-5px">
      <el-col :span="6" :lg="6" :md="6" :sm="24" :xs="24" class="column-height">
        <el-card class="rounded-md dark:bg-black gauge-card" shadow="hover">
          <GaugeChart></GaugeChart>
        </el-card>
        <el-card class="rounded-md dark:bg-black line-card m-t-10px" shadow="hover">
          <LineChart></LineChart>
        </el-card>
      </el-col>
      <el-col :span="18" :lg="18" :md="18" :sm="24" :xs="24">
        <el-card class="rounded-md dark:bg-black full-height" shadow="hover">
          <TopicCard></TopicCard>
        </el-card>
      </el-col>
    </el-row>
    <DivideLine></DivideLine>
    <EventGraph3D></EventGraph3D>
  </div>
</template>

<script setup lang="ts" name="home">
import BasicInfoCard from "./components/BasicInfoCard.vue";
import WordCloudChart from "./components/WordCloudChart.vue";
import EmotionChart from "./components/EmotionChart.vue";
import LineChart from "./components/LineChart.vue";
import EventGraph3D from "../../components/Event3D/EventGraph3D.vue";
import TopicCard from "./components/TopicCard.vue";
import DashBoardTitle from "./components/DashBoardTitle.vue";
import GaugeChart from "./components/GaugeChart.vue";
import DivideLine from "./components/DivideLine.vue";
</script>

<style lang="scss" scoped>
.rounded-md {
  border-radius: 10px;
}
.dark\:bg-black {
  background-color: #ffffff;
}
.shadow\:hover {
  box-shadow: 0 4px 8px rgb(0 0 0 / 10%);
}
.m-t-5px {
  margin-top: 10px;
  margin-bottom: 10px;
}
.column-height {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}
.gauge-card {
  flex: 3; /* 4/10 of the total height */
}
.line-card {
  flex: 7; /* 6/10 of the total height */
}
.full-height {
  height: 100%;
}
.m-t-10px {
  margin-top: 10px;
}
</style>
