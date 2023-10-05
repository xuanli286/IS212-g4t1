import axios from "axios";
import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useConstantStore = defineStore('constant', () => {
    const hiringDepartment = ref([]);
    const countries = ref([]);
    const roleSkills = ref([]);
    const staffSkills = ref([]);
    const staff = ref({});
    const roles = ref({});

    axios.get('http://127.0.0.1:5000/get_dept_country/dept')
        .then((response) => {
            hiringDepartment.value = response.data.data;
        })
        .catch((error) => {
            console.log(error.message);
        })

    axios.get('http://127.0.0.1:5000/get_dept_country/country')
        .then((response) => {
            countries.value = response.data.data;
        })
        .catch((error) => {
            console.log(error.message);
        })

    axios.get('http://127.0.0.1:5000/staff')
        .then((response) => {
            let data = response.data.data.staff
            for (const item of data) {
                for (const key in item) {
                    if (item.hasOwnProperty(key)) {
                        staff.value[key] = item[key]['staff_FName'] + " " + item[key]['staff_LName'];
                    }
                }
            }
        })
        .catch((error) => {
            console.log(error.message);
        })

    axios.get('http://127.0.0.1:5000/get_all_role')
        .then((response) => {
            for (let i of response.data.data) {
                for (let key in i) {
                    roles.value[key] = i[key];
                }
            }
        })
        .catch((error) => {
            console.log(error.message);
        })

    function getSkills(roleName) {
        axios.get('http://127.0.0.1:5000/get_role_skill/' + roleName)
            .then((response) => {
                roleSkills.value = response.data.data;
            })
            .catch((error) => {
                console.log(error.message);
            })
        }

    function getStaffSkills(staffID) {
        axios.get('http://127.0.0.1:5000/get_staff_skill/' + staffID)
            .then((response) => {
                staffSkills.value = response.data.data;
            })
            .catch((error) => {
                console.log(error.message);
            })
    }


    return {
        hiringDepartment,
        countries,
        roleSkills,
        staffSkills,
        staff,
        roles,
        getSkills,
        getStaffSkills,
    };
})
