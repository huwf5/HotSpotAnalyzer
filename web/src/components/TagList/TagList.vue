<template>
  <el-tag
    v-for="tag in tags"
    :key="tag"
    class="tags"
    :closable="props.closable"
    :disable-transitions="false"
    @close="handleClose(tag)"
  >
    {{ tag }}
  </el-tag>
  <el-input
    v-if="inputVisible"
    ref="InputRef"
    v-model="inputValue"
    class="w-20"
    size="small"
    @keyup.enter="handleInputConfirm"
    @blur="handleInputConfirm"
  />
  <el-button v-else-if="$props.showAddTag" class="button-new-tag" size="small" @click="showInput" icon="Plus">标签</el-button>
</template>

<script setup lang="ts">
import { addTagApi, deleteTagApi } from "@/api/modules/white_list";
import { ElInput } from "element-plus";
import { nextTick, ref } from "vue";

const tags = defineModel<Set<string>>({ required: true });

const props = withDefaults(
  defineProps<{
    format?: string;
    showAddTag: boolean;
    closable?: boolean;
  }>(),
  {
    closable: false
  }
);

const inputValue = ref("");
const inputVisible = ref(false);
const InputRef = ref<InstanceType<typeof ElInput>>();

const handleClose = async (tag: string) => {
  tags.value.delete(tag);
  props.format &&
    (await deleteTagApi({ email_format: props.format, email_tag: tag }).catch(() => {
      tags.value.add(tag);
    }));
};

const showInput = () => {
  inputVisible.value = true;
  nextTick(() => {
    InputRef.value!.input!.focus();
  });
};

const handleInputConfirm = async () => {
  if (inputValue.value) {
    let tag = inputValue.value;
    tags.value.add(inputValue.value);
    props.format &&
      (await addTagApi({ email_format: props.format, email_tag: tag }).catch(() => {
        tags.value.delete(tag);
      }));
  }
  inputVisible.value = false;
  inputValue.value = "";
};
</script>

<style scoped lang="scss">
.tags {
  margin: 0 0 0 5px;
}
.w-20 {
  width: 60px;
  margin: 0 0 0 5px;
}
.button-new-tag {
  margin: 0 0 0 5px;
}
</style>
