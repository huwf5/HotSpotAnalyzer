<template>
  <div class="message_settings">
    <setting-panel setting-title="高危事件阈值">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="danger_heat_cond">热度阈值</el-checkbox>
        <div v-if="danger_heat_cond" class="setting_row">
          <label class="setting_text">阈值设置</label>
          <el-input-number v-model="danger_heat_limit" :min="0"></el-input-number>
        </div>
      </div>
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="danger_composed_limit">组合条件</el-checkbox>
        <div v-if="danger_composed_limit" class="setting_row">
          <Conditions v-model="danger_conds" />
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="预警事件阈值">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="warning_heat_cond">热度阈值</el-checkbox>
        <div v-if="warning_heat_cond" class="setting_row">
          <label class="setting_text">阈值设置</label>
          <el-input-number v-model="warning_heat_limit" :min="0" :max="danger_heat_limit"></el-input-number>
        </div>
      </div>
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="warning_composed_limit">组合条件</el-checkbox>
        <div v-if="warning_composed_limit" class="setting_row">
          <Conditions v-model="warning_conds" />
        </div>
      </div>
    </setting-panel>
    <setting-panel setting-title="默认设置">
      <div class="single_setting">
        <el-checkbox class="setting_row" v-model="star_danger_default">自动标记高危事件</el-checkbox>
      </div>
      <div class="single_setting">
        <div class="setting_row">
          <label class="setting_text">热度计算公式</label>
          <el-tooltip placement="right" content='输入"$"以查看所有可选的指标'>
            <icon :size="15"> <QuestionFilled /> </icon>
          </el-tooltip>
        </div>
        <FormulaInput v-model="heat_formula" class="setting_row" />
      </div>
    </setting-panel>
  </div>
</template>

<script setup lang="ts">
import icon from "../../components/el-icon/icon.vue";
import { ref, watch } from "vue";
import SettingPanel from "./components/SettingPanel.vue";
import Conditions from "./components/ComposedConditions.vue";
import FormulaInput from "./components/FormulaInput.vue";
import { Messages } from "@/api/interface";

const danger_heat_cond = ref(true);
const danger_heat_limit = ref(10000);
const danger_composed_limit = ref(false);

const warning_heat_cond = ref(true);
const warning_heat_limit = ref(9000);
const warning_composed_limit = ref(false);

const star_danger_default = ref(true);

const danger_conds = ref<Messages.SingleCond[]>([]);
const warning_conds = ref<Messages.SingleCond[]>([]);
const heat_formula = ref("");

watch(danger_heat_limit, (newVal, oldVal) => {
  if (newVal < oldVal && warning_heat_limit.value > newVal) warning_heat_limit.value = newVal;
});

//测试数据
heat_formula.value = "ln($upVote/100+$like*2+$share*5)";
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
