import { createStore } from "vuex";

export const store = createStore({
  state: {
    selectedDate: "2024-05-27"
  },
  mutations: {
    setSelectedDate(state, date) {
      state.selectedDate = date;
    }
  },
  actions: {
    updateSelectedDate({ commit }, date) {
      commit("setSelectedDate", date);
    }
  },
  getters: {
    getSelectedDate: state => state.selectedDate
  }
});
