<template>
  <el-popover :visible="display_popover" :width="width" placement="top" trigger="contextmenu">
    <template #reference>
      <el-input
        :model-value="display_str"
        id="input_ref"
        @focus="focusInput"
        @blur="blurInput"
        @input="handleChange($event)"
        maxlength="200"
        show-word-limit
        clearable
        size="large"
      ></el-input>
    </template>
    <template #default>
      <div class="auto_complete" id="auto_complete_ref" v-click-outside="onClickOutside">
        <div v-for="(valPair, index) in mapValues" :key="index" style="margin: 2px 5px">
          <el-button @click="handleAutoComplete(index)">{{ valPair[2] }}</el-button>
        </div>
      </div>
    </template>
  </el-popover>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from "vue";

interface input_interface {
  selectionStart: number;
}

const input_node = ref<input_interface | null>(null);
const display_str = ref("");
const input_str = defineModel<string>({ required: true });
const display_popover = ref(false);
const width = ref(150);
// 第一部分为自动补全填入的内容，第二部分为展示内容，第三部分为自动补全的选项内容
const mapValues = ref<[string, string, string][]>([
  ["$upVote", "@[点击数]", "点击数"],
  ["$like", "@[喜爱数]", "喜爱数"],
  ["$share", "@[转发数]", "转发数"],
  ["$e", "e", "自然常数"]
]);

nextTick(() => {
  input_node.value = document.getElementById("input_ref") as unknown as input_interface;
  let auto_complete = document.getElementById("auto_complete_ref");
  if (auto_complete) width.value = auto_complete.getBoundingClientRect().width;
});

function focusInput() {
  display_str.value = input_str.value;
}
async function display() {
  // input_str映射到display_str
  input_str.value = input_str.value.replaceAll(/[\t\s]+/g, "");

  await nextTick();

  display_str.value = input_str.value;
  mapValues.value.forEach(pair => {
    display_str.value = display_str.value.replaceAll(pair[0], pair[1]);
  });
}
async function blurInput() {
  if (!display_popover.value) {
    await display();
    if (display_str.value.includes("$")) throw SyntaxError("无法解析表达式，请检查表达式格式！");
  }
}
async function handleAutoComplete(index: number) {
  if (input_node.value === null) return;
  let selectionStart = input_node.value.selectionStart;
  input_str.value =
    (selectionStart > 0 ? input_str.value.substring(0, selectionStart - 1) : "") +
    mapValues.value[index][0] +
    (input_str.value.length > selectionStart ? input_str.value.substring(selectionStart) : "");
  await nextTick();
  await display();
  display_popover.value = false;
}
function handleChange(input: string) {
  display_str.value = input;
  input_str.value = input;
  if (input_node.value === null) return;
  let selectionStart = input_node.value.selectionStart;
  if (selectionStart > 0 && input[selectionStart - 1] === "$") display_popover.value = true;
  else display_popover.value = false;
}
function onClickOutside() {
  display_popover.value = false;
}

onMounted(display);
</script>

<style scoped lang="scss">
.auto_complete {
  position: static;
  display: flex;
  width: fit-content;
  height: fit-content;
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;

  flex: none;
  padding: 0px;
  margin: 0px;
}
</style>
