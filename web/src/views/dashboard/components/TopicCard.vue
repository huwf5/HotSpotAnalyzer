<template>
  <div class="projects-section-header">
    <p>👻概览</p>
    <p class="time">December, 12</p>
  </div>
  <div class="projects-section-line">
    <div class="projects-status">
      <div class="item-status">
        <span class="status-number">{{ num_of_topics }}</span>
        <span class="status-type">热门话题</span>
      </div>
      <div class="item-status">
        <span class="status-number">{{ num_of_comments }}</span>
        <span class="status-type">总讨论数</span>
      </div>
    </div>
    <div class="view-actions">
      <button class="view-btn list-view" title="List View" @click="setCurrentView('list')" :class="{ active: !isGridView }">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="feather feather-list"
        >
          <line x1="8" y1="6" x2="21" y2="6" />
          <line x1="8" y1="12" x2="21" y2="12" />
          <line x1="8" y1="18" x2="21" y2="18" />
          <line x1="3" y1="6" x2="3.01" y2="6" />
          <line x1="3" y1="12" x2="3.01" y2="12" />
          <line x1="3" y1="18" x2="3.01" y2="18" />
        </svg>
      </button>
      <button class="view-btn grid-view" title="Grid View" @click="setCurrentView('grid')" :class="{ active: isGridView }">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="feather feather-grid"
        >
          <rect x="3" y="3" width="7" height="7" />
          <rect x="14" y="3" width="7" height="7" />
          <rect x="14" y="14" width="7" height="7" />
          <rect x="3" y="14" width="7" height="7" />
        </svg>
      </button>
    </div>
  </div>
  <div class="project-boxes" :class="{ jsGridView: isGridView, jsListView: !isGridView }">
    <div class="project-box-wrapper" v-for="project in projects" :key="project.id">
      <div class="project-box" :style="{ backgroundColor: project.color }">
        <div class="project-box-header">
          <span>{{ project.date }}</span>
          <div class="more-wrapper">
            <button class="project-btn-more" @click="goToEventPage(project.title)">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="feather feather-more-vertical"
              >
                <circle cx="12" cy="12" r="1" />
                <circle cx="12" cy="5" r="1" />
                <circle cx="12" cy="19" r="1" />
              </svg>
            </button>
          </div>
        </div>
        <div class="project-box-content-header">
          <p class="box-content-header">{{ project.title }}</p>
          <p class="box-content-subheader">{{ project.description }}</p>
        </div>
        <div class="box-progress-wrapper">
          <p class="box-progress-header">{{ project.progressType }}</p>
          <div class="box-progress-bar">
            <span class="box-progress" :style="{ width: project.progress + '%', backgroundColor: project.progressColor }"></span>
          </div>
          <p class="box-progress-percentage">{{ project.progress }}%</p>
        </div>
        <div class="project-box-footer">
          <div class="days-left" :style="{ color: project.progressColor }">{{ project.footerText }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { getCardList } from "@/api/modules/event_analysis";
// import axios from "axios";

const isGridView = ref(true);
const setCurrentView = view => {
  isGridView.value = view === "grid";
};

const store = useStore();
const selectedDate = computed(() => store.getters.getSelectedDate);
const date = ref("");

const router = useRouter();

const defaultProject = {
  id: 1,
  date: "2024-06-29",
  title: "#默认话题#",
  description: "这是一个默认话题描述，显示在数据请求失败时。",
  progress: 50,
  progressType: "话题热度",
  progressColor: "#ff942e",
  footerText: "话题帖子数: 10",
  color: "#fee4cb"
};

// 使用 Array.fill 生成六个相同的默认项目
const defaultProjects = Array(6)
  .fill(defaultProject)
  .map((item, index) => ({
    ...item,
    id: index + 1
  }));

const fetchTopicCardData = async selectedDateValue => {
  if (selectedDateValue === "earlier") {
    date.value = "history";
  } else {
    date.value = selectedDateValue;
  }

  // const response = await axios.get(`http://127.0.0.1:8000/api/topiccard/fetch_topic_card/?date=${date.value}`, {
  //   headers: {
  //     Authorization:
  //       "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NTY5MzI3LCJpYXQiOjE3MTk1NDc3MjcsImp0aSI6IjRiMzQxY2NhYmRiYjQ3YTA5NmUyNTJhYWU0NDA5MjlhIiwidXNlcl9lbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIn0.SUWOSeM-Dq-cevFsq_rUCuSH5I3IG4Qi9alcp00DCXk", // 替换为你的JWT令牌
  //     accept: "application/json"
  //   }
  // });
  try {
    const response = await getCardList(date.value);
    // console.log(response);
    const data = response;
    num_of_topics.value = data["num_of_topics"];
    num_of_comments.value = data["num_of_comments"];

    projects.value = data["topic_list"].map((topicItem, index) => ({
      id: index + 1,
      date: topicItem.date,
      title: "#" + topicItem.title + "#",
      description: topicItem.summary,
      progress: Math.round(topicItem.progress * 100),
      progressType: "话题热度",
      progressColor: colorPairs[index % colorPairs.length].progressColor,
      footerText: "话题帖子数: " + topicItem.num_of_posts,
      color: colorPairs[index % colorPairs.length].color
    }));
  } catch (error) {
    projects.value = defaultProjects;
  }
};

interface Project {
  id: number;
  date: string;
  title: string;
  description: string;
  progress: number;
  progressType: string;
  progressColor: string;
  footerText: string;
  color: string;
}

// Watch for changes in selectedDate and fetch data accordingly
watch(
  selectedDate,
  newDate => {
    fetchTopicCardData(newDate);
  },
  { immediate: true }
);

// Define reactive variables for fetched data
const num_of_topics = ref(0);
const num_of_comments = ref(0);

const colorPairs = [
  { progressColor: "#ff942e", color: "#fee4cb" },
  { progressColor: "#4f3ff0", color: "#e9e7fd" },
  { progressColor: "#096c86", color: "#dbf6fd" },
  { progressColor: "#df3670", color: "#ffd3e2" },
  { progressColor: "#34c471", color: "#c8f7dc" },
  { progressColor: "#4067f9", color: "#d5deff" }
];

const projects = ref<Project[]>([]);

const goToEventPage = (title: string) => {
  // const encodedTitle = encodeURIComponent(title);
  // router.push(`/event?id=${encodedTitle}`);
  router.push(`/event/analysis/${title}`);
};
</script>
<style>
/* Scoped CSS here */
:root {
  --app-container: #f3f6fd;
  --main-color: #1f1c2e;
  --secondary-color: #4a4a4a;
  --link-color: #1f1c2e;
  --link-color-hover: #c3cff4;
  --link-color-active: #ffffff;
  --link-color-active-bg: #1f1c2e;
}
* {
  box-sizing: border-box;
}
.app-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1800px;
  height: 100%;
  background-color: var(--app-container);
  transition: 0.2s;
}
.app-container button,
.app-container input,
.app-container optgroup,
.app-container select,
.app-container textarea {
  font-family: "DM Sans", sans-serif;
}
.app-content {
  display: flex;
  height: 100%;
  padding: 16px 24px 24px 0;
  overflow: hidden;
}
.mode-switch {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  color: var(--main-color);
  background-color: transparent;
  border: none;
}
.projects-section-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 32px;
}
.projects-section-header {
  top: 0;
  left: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  color: #007bff;
}
.projects-section-header p {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  line-height: 32px;
  color: #007bff;
}
.projects-section-header .time {
  font-size: 20px;
}
.projects-status {
  display: flex;
}
.item-status {
  display: flex;
  flex-direction: column;
  margin-right: 16px;
}
.item-status:not(:last-child) .status-type::after {
  position: absolute;
  top: 50%;
  right: 8px;
  width: 6px;
  height: 6px;
  content: "";
  border: 1px solid var(--secondary-color);
  border-radius: 50%;
  transform: translateY(-50%);
}
.status-number {
  font-size: 24px;
  font-weight: 700;
  line-height: 32px;
  color: var(--main-color);
}
.status-type {
  position: relative;
  padding-right: 24px;
  color: var(--secondary-color);
}
.view-actions {
  display: flex;
  align-items: center;
}
.view-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 6px;
  margin-left: 8px;
  color: var(--main-color);
  background-color: transparent;
  border: none;
  border-radius: 4px;
  transition: 0.2s;
}
.view-btn.active {
  color: var(--link-color-active);
  background-color: var(--link-color-active-bg);
}
.view-btn:not(.active):hover {
  color: var(--link-color-active);
  background-color: var(--link-color-hover);
}
.project-boxes {
  max-height: 600px;
  margin: 0 -8px;
  overflow-y: auto;
}
.project-boxes.jsGridView {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  overflow-y: auto;
}
.project-boxes.jsGridView .project-box-wrapper {
  width: 33.3%;

  /* flex: 1 1 33%; */
}
.project-boxes.jsGridView .project-box {
  /* height: 325px; */
  display: flex;
  flex-direction: column; /* Makes items stack vertically */
  justify-content: space-between; /* Distributes space around items */
  margin-bottom: 16px;
}
.project-boxes.jsListView .project-box {
  position: relative;
  display: flex;
  border-radius: 10px;
}
.project-boxes.jsListView .project-box > * {
  margin-right: 24px;
}
.project-boxes.jsListView .more-wrapper {
  position: absolute;
  top: 16px;
  right: 16px;
}
.project-boxes.jsListView .project-box-content-header {
  order: 1;
  max-width: 120px;
}
.project-boxes.jsListView .project-box-header {
  order: 2;
}
.project-boxes.jsListView .project-box-footer {
  flex-direction: column;
  justify-content: flex-start;
  order: 3;
  padding-top: 0;
}
.project-boxes.jsListView .project-box-footer::after {
  display: none;
}
.project-boxes.jsListView .participants {
  margin-bottom: 8px;
}
.project-boxes.jsListView .project-box-content-header p {
  overflow: hidden;
  text-align: left;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.project-boxes.jsListView .project-box-header > span {
  position: absolute;
  bottom: 16px;
  left: 16px;
  font-size: 12px;
}
.project-boxes.jsListView .box-progress-wrapper {
  flex: 1;
  order: 3;
}
.project-box {
  --main-color-card: #dbf6fd;

  padding: 16px;
  background-color: var(--main-color-card);
  border-radius: 30px;
}
.project-box-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  color: var(--main-color);
}
.project-box-header span {
  font-size: 14px;
  line-height: 16px;
  color: #4a4a4a;
  opacity: 0.7;
}
.project-box-content-header {
  margin-bottom: 16px;
  text-align: center;
}
.project-box-content-header p {
  margin: 0;
}
.project-box-wrapper {
  padding: 8px;
  transition: 0.2s;
}
.project-btn-more {
  position: relative;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  padding: 0;
  background-color: transparent;
  border: none;
  transition: transform 0.3s ease;
}
.project-btn-more:hover {
  background-color: rgb(0 0 0 / 10%);
  transform: scale(1.1);
}
.more-wrapper {
  position: relative;
}
.box-content-header {
  font-size: 16px;
  font-weight: 700;
  line-height: 24px;
  opacity: 0.7;
}

/* .box-content-subheader {
  font-size: 14px;
  line-height: 24px;
  opacity: 0.7;
} */
.box-content-subheader {
  display: -webkit-box;
  overflow: hidden;
  font-size: 14px;
  line-height: 24px;
  text-overflow: ellipsis;
  white-space: normal;
  opacity: 0.7;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}
.box-progress {
  display: block;
  height: 4px;
  border-radius: 6px;
}
.box-progress-bar {
  width: 100%;
  height: 4px;
  margin: 8px 0;
  overflow: hidden;
  background-color: #ffffff;
  border-radius: 6px;
}
.box-progress-header {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  line-height: 16px;
}
.box-progress-percentage {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  line-height: 16px;
  text-align: right;
}
.project-box-footer {
  position: relative;
  display: flex;
  justify-content: space-between;
  padding-top: 16px;
}
.project-box-footer::after {
  position: absolute;
  top: 0;
  left: -16px;
  width: calc(100% + 32px);
  height: 1px;
  content: "";
  background-color: rgb(255 255 255 / 60%);
}
.days-left {
  flex-shrink: 0;
  padding: 6px 16px;
  font-size: 12px;
  font-weight: 700;
  background-color: rgb(255 255 255 / 60%);
  border-radius: 20px;
}
.mode-switch.active .moon {
  fill: var(--main-color);
}

@media screen and (width <= 980px) {
  .project-boxes.jsGridView .project-box-wrapper {
    width: 50%;
  }
  .status-number,
  .status-type {
    font-size: 14px;
  }
  .status-type::after {
    width: 4px;
    height: 4px;
  }
  .item-status {
    margin-right: 0;
  }
}

@media screen and (width <= 880px) {
  .messages-section {
    position: absolute;
    top: 0;
    z-index: 2;
    width: 100%;
    height: 100%;
    opacity: 0;
    transform: translateX(100%);
  }
  .messages-section .messages-close {
    display: block;
  }
  .messages-btn {
    display: flex;
  }
}

@media screen and (width <= 720px) {
  .app-name,
  .profile-btn span {
    display: none;
  }
  .add-btn,
  .notification-btn,
  .mode-switch {
    width: 20px;
    height: 20px;
  }
  .add-btn svg,
  .notification-btn svg,
  .mode-switch svg {
    width: 16px;
    height: 16px;
  }
}

@media screen and (width <= 520px) {
  .project-boxes {
    overflow-y: visible;
  }
  .app-sidebar,
  .app-icon {
    display: none;
  }
  .app-content {
    padding: 16px 12px 24px;
  }
  .status-number,
  .status-type {
    font-size: 10px;
  }
  .view-btn {
    width: 24px;
    height: 24px;
  }
  .project-boxes.jsGridView .project-box-wrapper {
    width: 100%;
  }
  .projects-section-header p,
  .projects-section-header .time {
    font-size: 18px;
  }
  .status-type {
    padding-right: 4px;
  }
  .status-type::after {
    display: none;
  }
  .messages-btn {
    top: 48px;
  }
  .box-content-header {
    font-size: 12px;
    line-height: 16px;
  }
  .box-content-subheader {
    font-size: 12px;
    line-height: 16px;
  }
  .project-boxes.jsListView .project-box-header > span {
    font-size: 10px;
  }
  .box-progress-header {
    font-size: 12px;
  }
  .box-progress-percentage {
    font-size: 10px;
  }
  .days-left {
    padding: 6px;
    font-size: 8px;
    text-align: center;
  }
  .project-boxes.jsListView .project-box > * {
    margin-right: 10px;
  }
  .project-boxes.jsListView .more-wrapper {
    top: 10px;
    right: 2px;
  }
}
</style>
