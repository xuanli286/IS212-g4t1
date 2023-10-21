import { createRouter, createWebHistory } from "vue-router";

import AddRoleListing from "../views/AddRoleListing.vue";
import EditRoleListing from "../views/EditRoleListing.vue";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import RoleListingManagement from "../views/RoleListingManagement.vue";
import SkillManagement from "../views/SkillManagement.vue";
import SkillProfile from "@/views/SkillProfile.vue";
import StaffViewSpecificRoleListing from "@/views/StaffViewSpecificRoleListing.vue";
import SpecificRoleListing from "../views/SpecificRoleListing.vue";
import RoleListingStaff from "../views/RoleListingStaff.vue";

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
    {
      path: "/addrolelisting",
      name: "AddRoleListing",
      component: AddRoleListing,
    },
    {
      path: "/editrolelisting/:id",
      name: "EditRoleListing",
      component: EditRoleListing,
    },
    {
      path: "/viewspecificrolelisting/:id",
      name: "StaffViewSpecificRoleListing",
      component: StaffViewSpecificRoleListing,
    },
    {
      path: "/specificrolelisting/:id",
      name: "SpecificRoleListing",
      component: SpecificRoleListing,
    },
    {
      path: "/rolelistingstaff",
      name: "Role Listing Staff",
      component: RoleListingStaff,
    },
    {
      path: "/skillprofile",
      name: "SkillProfile",
      component: SkillProfile,
    },
  ],
});

export default router;
