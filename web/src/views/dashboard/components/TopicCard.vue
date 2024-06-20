<template>
  <div class="projects-section-header">
    <p>👻概览</p>
    <p class="time">December, 12</p>
  </div>
  <div class="projects-section-line">
    <div class="projects-status">
      <div class="item-status">
        <span class="status-number">45</span>
        <span class="status-type">热门话题</span>
      </div>
      <div class="item-status">
        <span class="status-number">2400</span>
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
            <button class="project-btn-more">
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
import { ref } from "vue";
const isGridView = ref(true);
const setCurrentView = view => {
  isGridView.value = view === "grid";
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
const projects = ref<Project[]>([
  {
    id: 1,
    date: "December 10, 2020",
    title: "#小米联合创始人夫妇向中山大学捐赠1亿元#",
    description:
      "据中山大学微博消息，今日下午，林斌刘向东校友伉俪向中山大学捐赠签约仪式在中山大学广州校区南校园怀士堂举行，林斌刘向东夫妇向中山大学捐赠现金1亿元人民币。",
    progress: 60,
    progressType: "话题热度",
    progressColor: "#ff942e",
    footerText: "话题帖子数: 1000",
    color: "#fee4cb"
  },
  {
    id: 2,
    date: "December 10, 2020",
    title: "#小米联合创始人夫妇向中山大学捐赠1亿元#",
    description:
      "据中山大学微博消息，今日下午，林斌刘向东校友伉俪向中山大学捐赠签约仪式在中山大学广州校区南校园怀士堂举行，林斌刘向东夫妇向中山大学捐赠现金1亿元人民币。",
    progress: 60,
    progressType: "话题热度",
    progressColor: "#4f3ff0",
    footerText: "话题帖子数: 1000",
    color: "#e9e7fd"
  },
  {
    id: 3,
    date: "December 10, 2020",
    title: "#小米联合创始人夫妇向中山大学捐赠1亿元#",
    description:
      "据中山大学微博消息，今日下午，林斌刘向东校友伉俪向中山大学捐赠签约仪式在中山大学广州校区南校园怀士堂举行，林斌刘向东夫妇向中山大学捐赠现金1亿元人民币。",
    progress: 60,
    progressType: "话题热度",
    progressColor: "#096c86",
    footerText: "话题帖子数: 1000",
    color: "#dbf6fd"
  },
  {
    id: 4,
    date: "December 10, 2020",
    title: "#小米联合创始人夫妇向中山大学捐赠1亿元#",
    description:
      "据中山大学微博消息，今日下午，林斌刘向东校友伉俪向中山大学捐赠签约仪式在中山大学广州校区南校园怀士堂举行，林斌刘向东夫妇向中山大学捐赠现金1亿元人民币。",
    progress: 60,
    progressType: "话题热度",
    progressColor: "#df3670",
    footerText: "话题帖子数: 1000",
    color: "#ffd3e2"
  },
  {
    id: 5,
    date: "December 10, 2020",
    title: "#小米联合创始人夫妇向中山大学捐赠1亿元#",
    description:
      "据中山大学微博消息，今日下午，林斌刘向东校友伉俪向中山大学捐赠签约仪式在中山大学广州校区南校园怀士堂举行，林斌刘向东夫妇向中山大学捐赠现金1亿元人民币。",
    progress: 60,
    progressType: "话题热度",
    progressColor: "#34c471",
    footerText: "话题帖子数: 1000",
    color: "#c8f7dc"
  },
  {
    id: 6,
    date: "December 10, 2020",
    title: "#小米联合创始人夫妇向中山大学捐赠1亿元#",
    description:
      "据中山大学微博消息，今日下午，林斌刘向东校友伉俪向中山大学捐赠签约仪式在中山大学广州校区南校园怀士堂举行，林斌刘向东夫妇向中山大学捐赠现金1亿元人民币。",
    progress: 60,
    progressType: "话题热度",
    progressColor: "#4067f9",
    footerText: "话题帖子数: 1000",
    color: "#d5deff"
  }
  // Additional projects can be added here
]);
</script>
<style>
/* Scoped CSS here */
:root {
  --app-container: #f3f6fd;
  --main-color: #1f1c2e;
  --secondary-color: #4a4a4a;
  --link-color: #1f1c2e;
  --link-color-hover: #c3cff4;
  --link-color-active: #fff;
  --link-color-active-bg: #1f1c2e;
  --projects-section: #fff;
}
* {
  box-sizing: border-box;
}
.app-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--app-container);
  transition: 0.2s;
  max-width: 1800px;
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
  overflow: hidden;
  padding: 16px 24px 24px 0;
}

.mode-switch {
  background-color: transparent;
  border: none;
  padding: 0;
  color: var(--main-color);
  display: flex;
  justify-content: center;
  align-items: center;
}

.projects-section {
  flex: 2;
  background-color: var(--projects-section);
  border-radius: 32px;
  padding: 32px 32px 0 32px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.projects-section-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 32px;
}
.projects-section-header {
  display: flex;
  top: 0;
  left: 10px;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  color: #007bff;
}
.projects-section-header p {
  font-size: 18px;
  line-height: 32px;
  font-weight: 700;
  margin: 0;
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
.item-status:not(:last-child) .status-type:after {
  content: "";
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translatey(-50%);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  border: 1px solid var(--secondary-color);
}

.status-number {
  font-size: 24px;
  line-height: 32px;
  font-weight: 700;
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
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 6px;
  border-radius: 4px;
  background-color: transparent;
  border: none;
  color: var(--main-color);
  margin-left: 8px;
  transition: 0.2s;
}
.view-btn.active {
  background-color: var(--link-color-active-bg);
  color: var(--link-color-active);
}
.view-btn:not(.active):hover {
  background-color: var(--link-color-hover);
  color: var(--link-color-active);
}

.project-boxes {
  margin: 0 -8px;
  overflow-y: auto;
  max-height: 600px;
}
.project-boxes.jsGridView {
  display: flex;
  flex-wrap: wrap;
  overflow-y: auto;
}
.project-boxes.jsGridView .project-box-wrapper {
  width: 33.3%;
}
.project-boxes.jsListView .project-box {
  display: flex;
  border-radius: 10px;
  position: relative;
}
.project-boxes.jsListView .project-box > * {
  margin-right: 24px;
}
.project-boxes.jsListView .more-wrapper {
  position: absolute;
  right: 16px;
  top: 16px;
}
.project-boxes.jsListView .project-box-content-header {
  order: 1;
  max-width: 120px;
}
.project-boxes.jsListView .project-box-header {
  order: 2;
}
.project-boxes.jsListView .project-box-footer {
  order: 3;
  padding-top: 0;
  flex-direction: column;
  justify-content: flex-start;
}
.project-boxes.jsListView .project-box-footer:after {
  display: none;
}
.project-boxes.jsListView .participants {
  margin-bottom: 8px;
}
.project-boxes.jsListView .project-box-content-header p {
  text-align: left;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.project-boxes.jsListView .project-box-header > span {
  position: absolute;
  bottom: 16px;
  left: 16px;
  font-size: 12px;
}
.project-boxes.jsListView .box-progress-wrapper {
  order: 3;
  flex: 1;
}

.project-box {
  --main-color-card: #dbf6fd;
  border-radius: 30px;
  padding: 16px;
  background-color: var(--main-color-card);
}
.project-box-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  color: var(--main-color);
}
.project-box-header span {
  color: #4a4a4a;
  opacity: 0.7;
  font-size: 14px;
  line-height: 16px;
}
.project-box-content-header {
  text-align: center;
  margin-bottom: 16px;
}
.project-box-content-header p {
  margin: 0;
}
.project-box-wrapper {
  padding: 8px;
  transition: 0.2s;
}

.project-btn-more {
  padding: 0;
  height: 14px;
  width: 24px;
  height: 24px;
  position: relative;
  background-color: transparent;
  border: none;
  flex-shrink: 0;
  &:after,
  &:before {
    content: "";
    position: absolute;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--main-color);
    opacity: 0.8;
    left: 50%;
    transform: translatex(-50%);
  }

  &:before {
    top: 0;
  }
  &:after {
    bottom: 0;
  }
}

.more-wrapper {
  position: relative;
}

.box-content-header {
  font-size: 16px;
  line-height: 24px;
  font-weight: 700;
  opacity: 0.7;
}

.box-content-subheader {
  font-size: 14px;
  line-height: 24px;
  opacity: 0.7;
}

.box-progress {
  display: block;
  height: 4px;
  border-radius: 6px;
}
.box-progress-bar {
  width: 100%;
  height: 4px;
  border-radius: 6px;
  overflow: hidden;
  background-color: #fff;
  margin: 8px 0;
}
.box-progress-header {
  font-size: 14px;
  font-weight: 700;
  line-height: 16px;
  margin: 0;
}
.box-progress-percentage {
  text-align: right;
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  line-height: 16px;
}

.project-box-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 16px;
  position: relative;
}
.project-box-footer:after {
  content: "";
  position: absolute;
  background-color: rgba(255, 255, 255, 0.6);
  width: calc(100% + 32px);
  top: 0;
  left: -16px;
  height: 1px;
}

.days-left {
  background-color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  border-radius: 20px;
  flex-shrink: 0;
  padding: 6px 16px;
  font-weight: 700;
}

.mode-switch.active .moon {
  fill: var(--main-color);
}

@media screen and (max-width: 980px) {
  .project-boxes.jsGridView .project-box-wrapper {
    width: 50%;
  }

  .status-number,
  .status-type {
    font-size: 14px;
  }

  .status-type:after {
    width: 4px;
    height: 4px;
  }

  .item-status {
    margin-right: 0;
  }
}
@media screen and (max-width: 880px) {
  .messages-section {
    transform: translateX(100%);
    position: absolute;
    opacity: 0;
    top: 0;
    z-index: 2;
    height: 100%;
    width: 100%;
  }
  .messages-section .messages-close {
    display: block;
  }

  .messages-btn {
    display: flex;
  }
}
@media screen and (max-width: 720px) {
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

  .app-header-right button {
    margin-left: 4px;
  }
}
@media screen and (max-width: 520px) {
  .projects-section {
    overflow: auto;
  }

  .project-boxes {
    overflow-y: visible;
  }

  .app-sidebar,
  .app-icon {
    display: none;
  }

  .app-content {
    padding: 16px 12px 24px 12px;
  }

  .status-number,
  .status-type {
    font-size: 10px;
  }

  .view-btn {
    width: 24px;
    height: 24px;
  }

  .app-header {
    padding: 16px 10px;
  }

  .search-input {
    max-width: 120px;
  }

  .project-boxes.jsGridView .project-box-wrapper {
    width: 100%;
  }

  .projects-section {
    padding: 24px 16px 0 16px;
  }

  .app-header {
    padding: 10px;
  }

  .projects-section-header p,
  .projects-section-header .time {
    font-size: 18px;
  }

  .status-type {
    padding-right: 4px;
  }
  .status-type:after {
    display: none;
  }

  .search-input {
    font-size: 14px;
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
    font-size: 8px;
    padding: 6px 6px;
    text-align: center;
  }

  .project-boxes.jsListView .project-box > * {
    margin-right: 10px;
  }

  .project-boxes.jsListView .more-wrapper {
    right: 2px;
    top: 10px;
  }
}
</style>
