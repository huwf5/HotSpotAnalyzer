<template>
  <div class="management_container card">
    <ProTable
      :request-api="getWhiteListApi"
      :columns="columns"
      ref="proTable"
      @reload="refreshTags"
      :filter-callback="filterData"
    >
      <template #tableHeader="scope">
        <el-button type="primary" plain round icon="Plus" @click="add_dialog = true">添加白名单</el-button>
        <el-button type="primary" plain round :icon="edit_tag ? 'Unlock' : 'Lock'" @click="edit_tag = !edit_tag">
          编辑标签
        </el-button>
        <el-button type="success" plain round icon="Check" @click="handleActivateAll" :disabled="!scope.isSelected">
          全部启用
        </el-button>
        <el-button type="danger" plain round icon="Close" @click="handleDeactivateAll" :disabled="!scope.isSelected">
          全部禁用
        </el-button>
      </template>
      <template #format="scope">
        <div class="format_container">
          <span>{{ scope.row.format }}</span>
          <TagList
            v-model="getTagSet(scope.row.format).value"
            :show-add-tag="edit_tag"
            :format="scope.row.format"
            :closable="edit_tag"
          />
        </div>
      </template>
      <template #is_active="scope">
        <el-switch
          v-model="scope.row['is_active']"
          active-text="启用"
          inactive-text="禁用"
          @change="handleStateChange(scope.row)"
        ></el-switch>
      </template>
      <template #operations="scope">
        <el-button type="primary" link icon="Delete" @click="handleDelete(scope.row)">删除</el-button>
      </template>
    </ProTable>
    <AddDialog
      v-model="add_dialog"
      @new-row="
        () => {
          proTable?.getTableList();
          refreshTags();
        }
      "
    />
  </div>
</template>

<script setup lang="ts">
import ProTable from "@/components/ProTable/index.vue";
import AddDialog from "./components/AddDialog.vue";
import TagList from "@/components/TagList/TagList.vue";
import { ColumnProps, ProTableInstance } from "@/components/ProTable/interface";
import { User, WhiteList } from "@/api/interface";
import { Ref, ref } from "vue";
import { useHandleData } from "@/hooks/useHandleData";
import {
  activateWhiteListApi,
  deactivateWhiteListApi,
  deleteFromWhiteListApi,
  getTagsApi,
  getWhiteListApi
} from "@/api/modules/white_list";
import { ElMessage, ElMessageBox } from "element-plus";

const proTable = ref<ProTableInstance>();
const add_dialog = ref(false);
const edit_tag = ref(false);
const tag_map = new Map<string, Ref<Set<string>>>();
const available_tags = ref<{ value: string; label: string }[]>([]);

const columns = ref<ColumnProps<User.ResUser>[]>([
  {
    type: "selection",
    fixed: "left"
  },
  {
    prop: "format",
    label: "邮箱后缀",
    search: {
      el: "input"
    },
    showOverflowTooltip: false
  },
  {
    prop: "is_active",
    label: "状态"
  },
  {
    prop: "operations",
    label: "操作",
    fixed: "right",
    width: 200
  },
  {
    isShow: false,
    enum: available_tags,
    search: {
      label: "标签",
      el: "select",
      key: "tag",
      props: { filterable: true, multiple: true }
    }
  }
]);
function filterData(data: any, params: any): any {
  let result: any[] = [];
  let target: string[] | undefined = params["tag"];
  let available_tags_set: Set<string> = new Set();

  available_tags.value = [];
  for (const dataRow of data) {
    getTagSet(dataRow["format"]).value.forEach(val => {
      if (!available_tags_set.has(val)) {
        available_tags.value.push({ value: val, label: val });
        available_tags_set.add(val);
      }
    });
    if (target === undefined) result.push(dataRow);
    else {
      let accept = true;
      target.forEach(str => {
        !getTagSet(dataRow["format"]).value.has(str) && (accept = false);
      });
      accept && result.push(dataRow);
    }
  }
  return result;
}
async function handleStateChange(row: WhiteList.ResWhiteList) {
  if (row.is_active) {
    await activateWhiteListApi({ format: row.format }, { loading: false }).catch(() => {
      row.is_active = false;
    });
  } else {
    await deactivateWhiteListApi({ format: row.format }, { loading: false }).catch(() => {
      row.is_active = true;
    });
  }
}
function handleDelete(row: WhiteList.ResWhiteList) {
  ElMessageBox.confirm("删除白名单将会清除等待列表中属于该邮箱后缀的用户，是否继续？", "警告", {
    type: "warning",
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    draggable: true
  }).then(async () => {
    await deleteFromWhiteListApi({ format: row.format }).then(() => {
      ElMessage({
        type: "success",
        message: "删除成功"
      });
      proTable.value?.getTableList();
    });
  });
}
async function handleDeactivateAll() {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let deactivate_list: WhiteList.ReqOnWhiteList[] = [];
    selected_list.forEach(val => deactivate_list.push({ format: val.format }));
    await useHandleData(deactivateWhiteListApi, deactivate_list, "全部禁用").then(() => {
      selected_list.forEach(row => {
        row.is_active = false;
      });
    });
  }
}
async function handleActivateAll() {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let activate_list: WhiteList.ReqOnWhiteList[] = [];
    selected_list.forEach(val => activate_list.push({ format: val.format }));
    await useHandleData(activateWhiteListApi, activate_list, "全部启用").then(() => {
      selected_list.forEach(row => {
        row.is_active = true;
      });
    });
  }
}
function getTagSet(format: string) {
  if (!tag_map.has(format)) {
    tag_map.set(format, ref<Set<string>>(new Set()));
  }
  return tag_map.get(format)!;
}
function refreshTags() {
  getTagsApi().then(response => {
    response.data.forEach(item => {
      getTagSet(item.email_format).value.add(item.email_tag);
    });
  });
}
refreshTags();
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
