import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      results: {}
    };
  },
  mutations: {
    setResultFiles(state, { courseId, files }) {
      state.results[courseId] = files;
    }
  },
  actions: {
    updateResultFiles({ commit }, { courseId, files }) {
      commit('setResultFiles', { courseId, files });
    }
  },
  getters: {
    getResultFiles: (state) => (courseId) => {
      return state.results[courseId] || [];
    }
  }
});

export default store;
