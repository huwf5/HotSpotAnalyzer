<template>
  <div class="message-settings card">
    <setting-panel setting-title="预警消息阈值">
      <div class="single-setting">
        <div class="setting-row">
          <span>高于{{ userSettings.warning_threshold }}%</span>
          <div class="slider-wrapper">
            <el-slider v-model="userSettings.warning_threshold" :step="1" :min="0" :max="100" @input="handleInput(0)" />
          </div>
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="提醒消息阈值">
      <div class="single-setting">
        <div class="setting-row">
          <span>高于{{ userSettings.info_threshold }}%</span>
          <div class="slider-wrapper">
            <el-slider v-model="userSettings.info_threshold" :step="1" :min="0" :max="100" @input="handleInput(1)" />
          </div>
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
import { ElMessage, ElNotification } from "element-plus";
import { useHandleData } from "@/hooks/useHandleData";
import { useRouter } from "vue-router";
import { useTabsStore } from "@/stores/modules/tabs";
import { useUserStore } from "@/stores/modules/user";

const router = useRouter();
const store = useUserStore();
const tabStore = useTabsStore();

const userSettings = ref<Messages.ResMessageSetting>({
  allow_non_news: true,
  warning_threshold: 70,
  info_threshold: 50
});
const timerId = ref<NodeJS.Timeout>();
async function upload(params: Messages.ResMessageSetting) {
  await uploadMessageSettingsApi({
    allow_non_news: params.allow_non_news,
    warning_threshold: params.warning_threshold / 100,
    info_threshold: params.info_threshold / 100
  }).then(() => {
    ElNotification({
      title: "同步成功",
      type: "success",
      duration: 2000
    });
  });
}
function initPage() {
  getMessageSettingsApi()
    .then(response => {
      userSettings.value = {
        allow_non_news: response.data.allow_non_news,
        warning_threshold: response.data.warning_threshold * 100,
        info_threshold: response.data.info_threshold * 100
      };
      const unwatch = watch(
        userSettings,
        () => {
          if (timerId.value !== null) {
            clearTimeout(timerId.value);
          }
          timerId.value = setTimeout(() => {
            upload(userSettings.value);
            timerId.value = undefined;
          }, 2000);
        },
        { deep: true }
      );
      onUnmounted(unwatch);
    })
    .catch(e => {
      if (e.response.data.message && (e.response.data.message as string).includes("消息设置不存在")) {
        ElMessage.success({ message: "已同步数据" });
        localStorage.removeItem(`msg_settings_${store.userInfo.contactInfo.email}`);
        tabStore.removeTabs(router.currentRoute.value.fullPath);
        router.back();
      }
    });
}
function handleInput(target: number) {
  if (userSettings.value.warning_threshold < userSettings.value.info_threshold) {
    switch (target) {
      case 0:
        // warning changed
        userSettings.value.info_threshold = userSettings.value.warning_threshold;
        break;
      case 1:
        // info changed
        userSettings.value.warning_threshold = userSettings.value.info_threshold;
        break;
      default:
        break;
    }
  }
}
onBeforeUnmount(async () => {
  if (timerId.value) {
    clearTimeout(timerId.value);
    await upload(userSettings.value);
  }
});
localStorage.getItem(`msg_settings_${store.userInfo.contactInfo.email}`) !== null
  ? initPage()
  : useHandleData(createMessageSettingsApi, null, "开启消息通知服务", "info")
      .then(() => {
        localStorage.setItem(`msg_settings_${store.userInfo.contactInfo.email}`, "y");
        initPage();
      })
      .catch(e => {
        if (e && e.response.data.message && (e.response.data.message as string).includes("消息设置已存在")) {
          ElMessage.success({ message: "已同步数据" });
          localStorage.setItem(`msg_settings_${store.userInfo.contactInfo.email}`, "y");
          initPage();
        } else {
          tabStore.removeTabs(router.currentRoute.value.fullPath);
          router.back();
        }
      });
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
