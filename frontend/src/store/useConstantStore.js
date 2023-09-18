import axios from "axios";
import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useConstantStore = defineStore('constant', () => {
    const hiringDepartment = ref([]);
    const countries = ref([]);

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


    return {
        hiringDepartment,
        countries,
    }
})
