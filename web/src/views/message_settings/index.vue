<template>
  <div class="message_settings card">
    <setting-panel setting-title="高危事件阈值">
      <!-- <div class="single_setting">
        <el-checkbox class="setting_row" v-model="userSettings.use_danger_heat_limit">热度阈值</el-checkbox>
        <div v-if="userSettings.use_danger_heat_limit" class="setting_row">
          <label class="setting_text">阈值设置</label>
          <el-input-number v-model="userSettings.danger_heat_limit" :min="0"></el-input-number>
        </div>
      </div> -->
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="userSettings.use_danger_composed_limits">组合条件</el-checkbox>
        <div v-if="userSettings.use_danger_composed_limits" class="setting_row">
          <Conditions v-model="userSettings.danger_composed_limits" />
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="预警事件阈值">
      <!-- <div class="single_setting">
        <el-checkbox class="setting_row" v-model="userSettings.use_warning_heat_limit">热度阈值</el-checkbox>
        <div v-if="userSettings.use_warning_heat_limit" class="setting_row">
          <label class="setting_text">阈值设置</label>
          <el-input-number
            v-model="userSettings.warning_heat_limit"
            :min="0"
            :max="userSettings.danger_heat_limit"
          ></el-input-number>
        </div>
      </div> -->
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="userSettings.use_warning_composed_limits">组合条件</el-checkbox>
        <div v-if="userSettings.use_warning_composed_limits" class="setting_row">
          <Conditions v-model="userSettings.warning_composed_limits" />
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="默认设置">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="userSettings.auto_star">自动标记高危事件</el-checkbox>
      </div>
      <!-- <div class="single_setting">
        <div class="setting_row">
          <label class="setting_text">热度计算公式</label>
          <el-tooltip placement="right" content='输入"$"以查看所有可选的指标'>
            <icon>
              <QuestionFilled />
            </icon>
          </el-tooltip>
        </div>
        <FormulaInput v-model="userSettings.heat_formula" class="setting_row" />
      </div> -->
    </setting-panel>
  </div>
</template>

<script setup lang="ts">
// import icon from "@/components/el-icon/icon.vue";
// import FormulaInput from "./components/FormulaInput.vue";

import { ref, watch } from "vue";
import SettingPanel from "@/components/SettingPanel/index.vue";
import Conditions from "./components/ComposedConditions.vue";
import { fetchMessagesSettingsApi, uploadMessagesSettingsApi } from "@/api/modules/message_settings";
import { Messages } from "@/api/interface";
import { ElNotification } from "element-plus";

const userSettings = ref<Messages.ResMessageSettings>({
  // use_danger_heat_limit: true,
  // danger_heat_limit: 1000,
  // use_warning_heat_limit: true,
  // warning_heat_limit: 900,
  // heat_formula: "",
  danger_composed_limits: [],
  warning_composed_limits: [],
  auto_star: false,
  use_danger_composed_limits: false,
  use_warning_composed_limits: false
});
const timerId = ref<number | null>(null);
function upload(params: Messages.ResMessageSettings) {
  uploadMessagesSettingsApi(params).then(() => {
    ElNotification({
      title: "同步成功",
      type: "success",
      duration: 2000
    });
  });
}
fetchMessagesSettingsApi().then(response => {
  userSettings.value = response.data;
  watch(
    userSettings,
    () => {
      if (timerId.value !== null) {
        clearTimeout(timerId.value);
      }
      timerId.value = setTimeout(upload, 2000);
    },
    { deep: true }
  );
});
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
