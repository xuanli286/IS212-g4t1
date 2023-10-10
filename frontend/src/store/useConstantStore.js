import axios from "axios";
import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useConstantStore = defineStore('constant', () => {
    const hiringDepartment = ref([]);
    const countries = ref([]);
    const staff = ref({});
    const backend_url = ref("http://13.212.177.124:5000");

    axios.get(`${backend_url.value}/get_dept_country/dept`)
        .then((response) => {
            hiringDepartment.value = response.data.data.slice(2);
        })
        .catch((error) => {
            console.log(error.message);
        })

    axios.get(`${backend_url.value}/get_dept_country/country`)
        .then((response) => {
            countries.value = response.data.data;
        })
        .catch((error) => {
            console.log(error.message);
        })

    axios.get(`${backend_url.value}/staff`)
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


    return {
        hiringDepartment,
        countries,
        staff,
        backend_url
    }
})
