import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("can-user")),
  }),

  getters: {
    isLogged: (state) => !!state.user,
  },

  actions: {
    login(email) {
      const user = {
        email,
        role: "admin",
      };

      this.user = user;
      localStorage.setItem("can-user", JSON.stringify(user));
    },

    logout() {
      this.user = null;
      localStorage.removeItem("can-user");
    },
  },
});
