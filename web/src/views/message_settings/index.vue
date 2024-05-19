<template>
  <div class="message_settings card">
    <setting-panel setting-title="高危事件阈值">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="danger_heat_cond">热度阈值</el-checkbox>
        <div v-if="danger_heat_cond" class="setting_row">
          <label class="setting_text">阈值设置</label>
          <el-input-number v-model="userSettings.danger_heat_limit" :min="0"></el-input-number>
        </div>
      </div>
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="danger_composed_limit">组合条件</el-checkbox>
        <div v-if="danger_composed_limit" class="setting_row">
          <Conditions v-model="userSettings.danger_composed_limits" />
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="预警事件阈值">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="warning_heat_cond">热度阈值</el-checkbox>
        <div v-if="warning_heat_cond" class="setting_row">
          <label class="setting_text">阈值设置</label>
          <el-input-number
            v-model="userSettings.warning_heat_limit"
            :min="0"
            :max="userSettings.danger_heat_limit"
          ></el-input-number>
        </div>
      </div>
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="warning_composed_limit">组合条件</el-checkbox>
        <div v-if="warning_composed_limit" class="setting_row">
          <Conditions v-model="userSettings.warning_composed_limits" />
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="默认设置">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="userSettings.auto_star">自动标记高危事件</el-checkbox>
      </div>
      <div class="single_setting">
        <div class="setting_row">
          <label class="setting_text">热度计算公式</label>
          <el-tooltip placement="right" content='输入"$"以查看所有可选的指标'>
            <icon>
              <QuestionFilled />
            </icon>
          </el-tooltip>
        </div>
        <FormulaInput v-model="userSettings.heat_formula" class="setting_row" />
      </div>
    </setting-panel>
  </div>
</template>

<script setup lang="ts">
import icon from "@/components/el-icon/icon.vue";
import { ref, watch } from "vue";
import SettingPanel from "@/components/SettingPanel/index.vue";
import Conditions from "./components/ComposedConditions.vue";
import FormulaInput from "./components/FormulaInput.vue";
import { fetchMessagesSettingsApi, uploadMessagesSettingsApi } from "@/api/modules/message_settings";
import { Messages } from "@/api/interface";
import { ElNotification } from "element-plus";
// import { ElNotification } from "element-plus";

const userSettings = ref<Messages.ResMessageSettings>({
  danger_heat_limit: 1000,
  danger_composed_limits: [],
  warning_heat_limit: 900,
  warning_composed_limits: [],
  auto_star: false,
  heat_formula: "",
  use_danger_composed_limits: false,
  use_warning_composed_limits: false
});
const danger_heat_cond = ref(true);
const danger_composed_limit = ref(false);
const warning_heat_cond = ref(true);
const warning_composed_limit = ref(false);

watch(userSettings, newVal => {
  if (newVal.danger_heat_limit < newVal.warning_heat_limit) userSettings.value.warning_heat_limit = newVal.danger_heat_limit;
  uploadMessagesSettingsApi(newVal).then(response => {
    if (response.code !== "200") {
      ElNotification({
        title: "上传失败",
        message: response.code + " " + response.msg,
        type: "error",
        duration: 2000
      });
    }
  });
});
watch(danger_heat_cond, newVal => {
  if (newVal) {
    userSettings.value.danger_heat_limit =
      userSettings.value.danger_heat_limit < 0 ? -userSettings.value.danger_heat_limit : userSettings.value.danger_heat_limit;
  } else {
    userSettings.value.danger_heat_limit =
      userSettings.value.danger_heat_limit > 0 ? -userSettings.value.danger_heat_limit : userSettings.value.danger_heat_limit;
  }
});
watch(warning_heat_cond, newVal => {
  if (newVal) {
    userSettings.value.warning_heat_limit =
      userSettings.value.warning_heat_limit < 0 ? -userSettings.value.warning_heat_limit : userSettings.value.warning_heat_limit;
  } else {
    userSettings.value.warning_heat_limit =
      userSettings.value.warning_heat_limit > 0 ? -userSettings.value.warning_heat_limit : userSettings.value.warning_heat_limit;
  }
});
watch(danger_composed_limit, newVal => {
  userSettings.value.use_danger_composed_limits = newVal;
});
watch(warning_composed_limit, newVal => {
  userSettings.value.use_warning_composed_limits = newVal;
});
fetchMessagesSettingsApi().then(response => {
  if (response.code === "200") {
    userSettings.value = response.data;
    danger_heat_cond.value = userSettings.value.danger_heat_limit > 0;
    danger_composed_limit.value = userSettings.value.use_danger_composed_limits;

    warning_heat_cond.value = userSettings.value.warning_heat_limit > 0;
    warning_composed_limit.value = userSettings.value.use_warning_composed_limits;
  }
});
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
