<template>
  <div class="message-settings card">
    <setting-panel setting-title="预警消息阈值">
      <div class="single-setting">
        <div class="setting-row">
          <span>高于{{ userSettings.warning_threshold * 100 }}%</span>
          <el-slider v-model="userSettings.warning_threshold" :step="0.01" :min="0" :max="1"></el-slider>
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="提醒消息阈值">
      <div class="single-setting">
        <div class="setting-row">
          <span>高于{{ userSettings.info_threshold * 100 }}%</span>
          <el-slider
            v-model="userSettings.info_threshold"
            :step="0.01"
            :min="0"
            :max="userSettings.warning_threshold"
          ></el-slider>
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="默认设置">
      <div class="single-setting">
        <el-checkbox class="setting-row" v-model="userSettings.allow_non_news">允许接收非事件提醒消息</el-checkbox>
      </div>
    </setting-panel>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onUnmounted, ref, watch } from "vue";
import SettingPanel from "@/components/SettingPanel/index.vue";
import { createMessageSettingsApi, getMessageSettingsApi, uploadMessageSettingsApi } from "@/api/modules/message_settings";
import { Messages } from "@/api/interface";
import { ElNotification } from "element-plus";
import { useHandleData } from "@/hooks/useHandleData";
import { useRouter } from "vue-router";
import { useTabsStore } from "@/stores/modules/tabs";

const router = useRouter();
const tabStore = useTabsStore();

const userSettings = ref<Messages.ResMessageSetting>({
  allow_non_news: true,
  warning_threshold: 0.5,
  info_threshold: 0.5
});
const timerId = ref<NodeJS.Timeout | null>(null);
async function upload(params: Messages.ResMessageSetting) {
  await uploadMessageSettingsApi(params).then(() => {
    ElNotification({
      title: "同步成功",
      type: "success",
      duration: 2000
    });
  });
}
function initPage() {
  getMessageSettingsApi().then(response => {
    userSettings.value = response.data;
    const unwatch = watch(
      userSettings,
      () => {
        if (timerId.value !== null) {
          clearTimeout(timerId.value);
        }
        timerId.value = setTimeout(() => upload(userSettings.value), 2000);
      },
      { deep: true }
    );
    onUnmounted(unwatch);
  });
}
onBeforeUnmount(async () => {
  if (timerId.value) {
    clearTimeout(timerId.value);
    await upload(userSettings.value);
  }
});
localStorage.getItem("msg_settings") !== null
  ? initPage()
  : useHandleData(createMessageSettingsApi, null, "开启消息通知服务", "info")
      .then(() => {
        localStorage.setItem("msg_settings", "y");
        initPage();
      })
      .catch(() => {
        tabStore.removeTabs(router.currentRoute.value.fullPath);
        router.back();
      });
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
