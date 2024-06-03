<template>
  <div class="management_container card">
    <ProTable :request-api="getPendingListApi" :columns="columns" ref="proTable" :filter-callback="filterData">
      <template #tableHeader="scope">
        <el-button type="success" plain round icon="Check" @click="handleAcceptAll" :disabled="!scope.isSelected">
          全部通过
        </el-button>
        <el-button type="danger" plain round icon="Delete" @click="handleRejectAll" :disabled="!scope.isSelected">
          全部拒绝
        </el-button>
      </template>
      <template #email="scope">
        <div class="email_container">
          <span>{{ scope.row.email }}</span>
          <TagList v-model="getTagSet(scope.row.email).value" :show-add-tag="false" />
        </div>
      </template>
      <template #operations="scope">
        <el-button type="primary" link icon="Check" @click="acceptUser(scope.row)">通过</el-button>
        <el-button type="primary" link icon="Delete" @click="rejectUser(scope.row)">拒绝</el-button>
      </template>
    </ProTable>
  </div>
</template>

<script setup lang="ts">
import ProTable from "@/components/ProTable/index.vue";
import TagList from "@/components/TagList/TagList.vue";

import { getPendingListApi, activateUserApi, rejectActivationApi } from "@/api/modules/user_management";
import { ColumnProps, ProTableInstance } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { Ref, ref } from "vue";
import { useHandleData } from "@/hooks/useHandleData";
import { getTagsApi } from "@/api/modules/white_list";

const proTable = ref<ProTableInstance>();
const tag_map = new Map<string, Ref<Set<string>>>();
const available_tags = ref<{ value: string; label: string }[]>([]);

const columns = ref<ColumnProps<User.ResUser>[]>([
  {
    type: "selection",
    fixed: "left"
  },
  {
    prop: "username",
    label: "用户名",
    search: {
      el: "input",
      order: 1
    }
  },
  {
    prop: "email",
    label: "邮箱地址",
    search: {
      el: "input"
    }
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
    getTagSet(dataRow["email"]).value.forEach(val => {
      if (!available_tags_set.has(val)) {
        available_tags.value.push({ value: val, label: val });
        available_tags_set.add(val);
      }
    });
    if (target === undefined) result.push(dataRow);
    else {
      let accept = true;
      target.forEach(str => {
        !getTagSet(dataRow["email"]).value.has(str) && (accept = false);
      });
      accept && result.push(dataRow);
    }
  }
  return result;
}
async function rejectUser(params: User.ResPendingUser) {
  await useHandleData(rejectActivationApi, { emailList: [params.email] }, `拒绝${params.username}`).then(() => {
    // 刷新数据
    proTable.value?.getTableList();
  });
}
async function acceptUser(params: User.ResPendingUser) {
  await useHandleData(activateUserApi, { emailList: [params.email] }, `激活${params.username}`).then(() => {
    // 刷新数据
    proTable.value?.getTableList();
  });
}
async function handleRejectAll() {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let delete_list: string[] = [];
    selected_list.forEach(val => delete_list.push(val.email));
    await useHandleData(rejectActivationApi, { emailList: delete_list }, "全部删除").then(() => {
      proTable.value?.getTableList();
    });
  }
}
async function handleAcceptAll() {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let delete_list: string[] = [];
    selected_list.forEach(val => delete_list.push(val.email));
    await useHandleData(activateUserApi, { emailList: delete_list }, "全部激活").then(() => {
      proTable.value?.getTableList();
    });
  }
}
function getTagSet(format: string) {
  format = format.match(/@.*$/g)![0];
  if (!tag_map.has(format)) {
    tag_map.set(format, ref<Set<string>>(new Set()));
  }
  return tag_map.get(format)!;
}
function refreshTags() {
  getTagsApi().then(response => {
    tag_map.clear();
    available_tags.value = [];
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
