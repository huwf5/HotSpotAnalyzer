<template>
  <div class="management_container card">
    <ProTable :request-api="getUserList" :columns="columns" ref="proTable">
      <template #tableHeader>
        <el-button type="success" plain round icon="Check" @click="handleChangeAll(true)">启用</el-button>
        <el-button type="danger" plain round icon="Close" @click="handleChangeAll(false)">禁用</el-button>
        <el-button type="danger" plain round icon="Delete" @click="handleRemoveAll">删除</el-button>
      </template>
      <template #status="scope">
        <el-switch
          v-model="scope.row.status"
          active-text="启用"
          inactive-text="禁用"
          :active-value="1"
          :inactive-value="0"
          @click="changeState(scope.row)"
        ></el-switch>
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
import { batchChangeStatus, batchDeleteUser, getUserList, resetUserPassWord } from "@/api/modules/user_management";
import { ColumnProps, ProTableInstance } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { ref } from "vue";
import { useHandleData } from "@/hooks/useHandleData";
import { ElNotification } from "element-plus";

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
    prop: "id",
    label: "学工号",
    search: {
      el: "input",
      props: { maxlength: 20, showWordLimit: true, clearable: true },
      order: 1
    },
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
    prop: "status",
    label: "状态",
    enum: [
      { label: "启用", value: 1 },
      { label: "禁用", value: 0 }
    ],
    search: {
      el: "select",
      order: 2
    },
    width: 150
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
async function changeState(params: User.ResUser) {
  let change_list = new FormData();
  change_list.append(params.id, params.status === 0 ? "1" : "0");
  await useHandleData(
    batchChangeStatus,
    change_list,
    params.status === 0 ? `启用${params.username}` : `禁用${params.username}`
  ).catch(reason => {
    if (reason.code !== undefined) {
      // 取消，回滚
      params.status = 1 - params.status;
    }
  });
}
async function handleChangeAll(state: boolean) {
  let selected_list = proTable.value?.selectedList;
  if (selected_list) {
    if (selected_list.length === 0) return;
    let _Val = state ? "true" : "false";
    let pairs: FormData = new FormData();
    selected_list.forEach(val => pairs.append(val.id, _Val));
    await useHandleData(batchChangeStatus, pairs, `全部${state ? "激活" : "禁用"}`)
      .then(() => {
        proTable.value?.getTableList();
      })
      .catch(reason => {
        if (reason.code === undefined) {
          ElNotification({
            title: "错误",
            message: reason,
            type: "error",
            duration: 3000
          });
        }
      });
  }
}
async function resetUserPwd(params: User.ResUser) {
  await useHandleData(resetUserPassWord, { id: params.id }, `重置${params.username}密码`).catch(reason => {
    ElNotification({
      title: "错误",
      message: reason,
      type: "error",
      duration: 3000
    });
  });
}
async function removeUser(params: User.ResUser) {
  await useHandleData(batchDeleteUser, [params.id], `删除${params.username}`).then(() => {
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
    await useHandleData(batchDeleteUser, delete_list, "全部删除")
      .then(() => {
        proTable.value?.getTableList();
      })
      .catch(reason => {
        if (reason.code === undefined) {
          ElNotification({
            title: "错误",
            message: reason,
            type: "error",
            duration: 3000
          });
        }
      });
  }
}
</script>

<style scoped lang="scss">
@import "./index.scss";
</style>
