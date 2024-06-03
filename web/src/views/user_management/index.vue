<template>
  <div class="management_container card">
    <ProTable :request-api="getUserListApi" :columns="columns" ref="proTable" :filter-callback="filterField">
      <template #tableHeader="scope">
        <el-button type="danger" plain round icon="Delete" @click="handleRemoveAll" :disabled="!scope.isSelected">
          全部删除
        </el-button>
      </template>
      <template #email="scope">
        <div class="email_container">
          <span>{{ scope.row.email }}</span>
          <TagList v-model="getTagSet(scope.row.email).value" :show-add-tag="false" />
        </div>
      </template>
      <template #operations="scope">
        <el-button type="primary" link @click="changeUserPower(scope.row, true)">升级权限</el-button>
        <el-button type="primary" link @click="changeUserPower(scope.row, false)">降低权限</el-button>
        <el-button type="primary" link icon="Refresh" @click="resetUserPwd(scope.row)">重置密码</el-button>
        <el-button type="primary" link icon="Delete" @click="removeUser(scope.row)">删除</el-button>
      </template>
    </ProTable>
  </div>
</template>

<script setup lang="ts">
import ProTable from "@/components/ProTable/index.vue";
import TagList from "@/components/TagList/TagList.vue";

import {
  batchDeleteUserApi,
  batchDemoteUserApi,
  batchMandateUserApi,
  getRoleDictApi,
  getUserListApi,
  resetUserPassWordApi
} from "@/api/modules/user_management";
import { ColumnProps, EnumProps, ProTableInstance } from "@/components/ProTable/interface";
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
    fixed: "right"
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
function filterField(data: any, params: any): any {
  let result: any[] = [];
  let target_tags: string[] | undefined = params["tag"];
  let target_roles: string[] | undefined = params["role"];
  let available_tags_set: Set<string> = new Set();

  available_tags.value = [];
  for (const dataRow of data) {
    getTagSet(dataRow["email"]).value.forEach(val => {
      if (!available_tags_set.has(val)) {
        available_tags.value.push({ value: val, label: val });
        available_tags_set.add(val);
      }
    });
    let accept = true;
    target_tags &&
      target_tags.forEach(str => {
        !getTagSet(dataRow["email"]).value.has(str) && (accept = false);
      });
    target_roles && target_roles.length > 0 && !target_roles.includes(dataRow["role"]) && (accept = false);
    accept && result.push(dataRow);
  }
  return result;
}
getRoleDictApi().then(response => {
  let dict: EnumProps[] = [];
  response.data.forEach(item => dict.push({ value: item.id, label: item.role }));
  columns.value.push({
    prop: "role",
    label: "权限等级",
    enum: dict,
    search: {
      el: "select",
      order: 3,
      props: { filterable: true, multiple: true }
    },
    width: 200
  });
});
async function changeUserPower(params: User.ResUser, upgrade: boolean) {
  if (upgrade) {
    await useHandleData(batchMandateUserApi, { emailList: [params.email] }, `升级用户${params.username}权限`).then(() => {
      proTable.value?.getTableList();
    });
  } else {
    await useHandleData(batchDemoteUserApi, { emailList: [params.email] }, `降低用户${params.username}权限`).then(() => {
      proTable.value?.getTableList();
    });
  }
}
async function resetUserPwd(params: User.ResUser) {
  await useHandleData(resetUserPassWordApi, { id: params.email }, `重置${params.username}密码`);
}
async function removeUser(params: User.ResUser) {
  await useHandleData(batchDeleteUserApi, { emailList: [params.email] }, `删除${params.username}`).then(() => {
    // 刷新数据
    proTable.value?.getTableList();
  });
}
async function handleRemoveAll() {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let delete_list: string[] = [];
    selected_list.forEach(val => delete_list.push(val.email));
    await useHandleData(batchDeleteUserApi, { emailList: delete_list }, "全部删除").then(() => {
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
