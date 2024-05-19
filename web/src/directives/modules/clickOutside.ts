import { DirectiveBinding } from "vue";

// 定义全局指令 v-click-outside
const vClickOutside = {
  beforeMount(el: any, binding: DirectiveBinding<any>) {
    el.clickOutsideEvent = function (e: any) {
      // 点击的目标元素是否在指令绑定的元素内部
      const clickedInside = el.contains(e.target as Node) || el === e.target;
      // 如果点击的是内部元素并且绑定了回调函数，则执行回调
      if (!clickedInside && binding.value) {
        binding.value(e);
      }
    };
    // 绑定点击事件监听器到文档
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el: any) {
    // 在指令解绑时移除事件监听器
    document.removeEventListener("click", el.clickOutsideEvent);
  }
};

export default vClickOutside;
