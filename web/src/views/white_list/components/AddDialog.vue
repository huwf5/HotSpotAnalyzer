<template>
  <el-dialog v-model="add_dialog" title="添加白名单" @opened="focusOnInput">
    <div class="dialog_body">
      <span class="dialog_text" style="margin: 0 0 10px">输入邮箱后缀</span>
      <el-input name="postfix_input" v-model="add_item" placeholder='示例："example.com"或"@example.com"'></el-input>
      <span class="dialog_text" style="margin: 20px 0 10px">添加标签（可选）</span>
      <div class="tag_container"><TagList v-model="newTags" :show-add-tag="true" /></div>
    </div>
    <template #footer>
      <div class="footer">
        <el-button type="primary" @click="addToList" :loading="is_loading">确认</el-button>
        <el-button link @click="add_dialog = false">取消</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import TagList from "@/components/TagList/TagList.vue";
import { addTagApi, addToWhiteListApi } from "@/api/modules/white_list";
import { ElMessage } from "element-plus";
import { ref } from "vue";

const add_dialog = defineModel<boolean>({ required: true });
const newTags = ref<Set<string>>(new Set());
const add_item = ref("");
const is_loading = ref(false);

const emits = defineEmits<{
  newRow: any;
}>();

function focusOnInput() {
  let l = document.getElementsByName("postfix_input");
  if (l.length > 0) l.item(0).focus();
}
async function addToList() {
  is_loading.value = true;
  if (add_item.value.match(/^(@)?[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$/g) !== null) {
    let email_format = (add_item.value.charAt(0) !== "@" ? "@" : "") + add_item.value;
    await addToWhiteListApi({ format: email_format }).then(() => {
      newTags.value.forEach(async email_tag => {
        await addTagApi({ email_format, email_tag });
      });
      ElMessage({
        type: "success",
        message: "添加成功"
      });
      add_dialog.value = false;
      emits("newRow");
    });
    add_item.value = "";
  } else {
    ElMessage({
      type: "error",
      message: "格式错误"
    });
    focusOnInput();
  }
  is_loading.value = false;
}
</script>

<style scoped lang="scss">
.dialog_body {
  display: flex;
  flex: none;
  flex-direction: column;
  justify-content: flex-start;
}
.dialog_text {
  font-size: 13px;
  font-weight: 300;
  line-height: 29px;
  text-align: left;
  letter-spacing: 0;
}
.tag_container {
  display: flex;
  flex: none;
  flex-direction: row;
}
.footer {
  display: flex;
  flex: none;
  flex-direction: row;
  justify-content: flex-end;
}
</style>
