import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import SkillManagement from "../views/SkillManagement.vue";
import Login from "../views/Login.vue";
import AddRoleListing from "../views/AddRoleListing.vue";
import EditRoleListing from "../views/EditRoleListing.vue";

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
        path: "/skillmanagement",
        name: "SkillManagement",
        component: SkillManagement,
      },
      {
        path: "/",
        name: "Login",
        component: Login,
      },
      {
        path: "/addrolelisting",
        name: "AddRoleListing",
        component: AddRoleListing,
      },
      {
        path: "/editrolelisting/:id",
        name: "EditRoleListing",
        component: EditRoleListing,
      }
    ],
});

export default router;