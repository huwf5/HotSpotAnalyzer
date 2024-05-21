<template>
  <div class="management_container card">
    <ProTable :request-api="getUserList" :columns="columns" ref="proTable">
      <template #tableHeader>
        <el-button type="danger" plain round icon="Delete" @click="handleRemoveAll">删除</el-button>
      </template>
      <template #operations="scope">
        <el-button type="primary" link icon="Refresh" @click="resetUserPwd(scope.row)">重置密码</el-button>
        <el-button type="primary" link icon="Delete" @click="removeUser(scope.row)">删除</el-button>
      </template>
    </ProTable>
  </div>
</template>

<script setup lang="ts">
import ProTable from "@/components/ProTable/index.vue";
import { batchDeleteUser, getUserList, resetUserPassWord } from "@/api/modules/user_management";
import { ColumnProps, ProTableInstance } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { ref } from "vue";
import { useHandleData } from "@/hooks/useHandleData";

const proTable = ref<ProTableInstance>();

const columns = ref<ColumnProps<User.ResUser>[]>([
  {
    type: "selection",
    fixed: "left"
  },
  {
    prop: "createTime",
    width: 150,
    label: "申请时间",
    search: {
      el: "date-picker",
      span: 2,
      props: { type: "datetimerange", valueFormat: "YYYY-MM-DD" },
      order: 4
    }
  },
  {
    prop: "username",
    label: "用户名",
    width: 100
  },
  {
    prop: "auth",
    label: "权限等级",
    enum: [
      { label: "普通用户", value: 0 },
      { label: "管理员", value: 1 }
    ],
    search: {
      el: "select",
      order: 3
    },
    width: 100
  },
  {
    prop: "email",
    label: "邮箱地址"
  },
  {
    prop: "operations",
    label: "操作",
    fixed: "right",
    width: 200
  }
]);
async function resetUserPwd(params: User.ResUser) {
  await useHandleData(resetUserPassWord, { id: params.email }, `重置${params.username}密码`);
}
async function removeUser(params: User.ResUser) {
  await useHandleData(batchDeleteUser, [params.email], `删除${params.username}`).then(() => {
    // 刷新数据
    proTable.value?.getTableList();
  });
}
async function handleRemoveAll() {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let delete_list: string[] = [];
    selected_list.forEach(val => delete_list.push(val.id));
    await useHandleData(batchDeleteUser, delete_list, "全部删除").then(() => {
      proTable.value?.getTableList();
    });
  }
}
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
