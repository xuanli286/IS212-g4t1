import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import RoleListingManagement from "../views/RoleListingManagement.vue";
import SkillManagement from "../views/SkillManagement.vue";
import Login from "../views/Login.vue";

const router = createRouter({
  scrollBehavior(to, from, savedPosition) {
    // always scroll to top
    return { top: 0 };
  },
  history: createWebHistory(),
  routes: [
    {
      path: "/home",
      name: "Home",
      component: Home,
    },
    {
      path: "/rolelistingmanagement",
      name: "Role Listing Management",
      component: RoleListingManagement,
    },
    {
      path: "/skillmanagement",
      name: "SkillManagement",
      component: SkillManagement,
    },
    {
      path: "/",
      name: "Login",
      component: Login,
    },
  ],
});

export default router;
