<script setup>
import { useModalStore } from "@/store/useModalStore.js";
import { storeToRefs } from "pinia";

const store = useModalStore();
const { isOpen, isSuccess } = storeToRefs(store);

function closeModal() {
  isOpen.value = false;
  isSuccess.value = false;
}

function submitApplication() {
  // console.log("Hello");
  const body = {
    staff_ID: this.currentUser.staff_ID,
    rolelisting_ID: rolelistingID,
    application_date: new Date().toISOString().slice(0, 10),
    percentage_match: getSkillPercentage()
  };
  console.log(body);
  axios
    .post(`${this.backend_url}/addapplication`, body)
    .then((response) => {
      console.log(response);
      this.applicationSuccess = true;
    })
    .catch((error) => {
      console.log(error.message);
      this.applicationSuccess = false;
    });
  document.getElementById("confirm-modal").classList.remove("hidden");
}
function getSkillPercentage() {
      let match = 0;
      // THIS PART IS AN ISSUE BECAUSE I NEED TO GET SKILLS FROM THE SPECIFICROLELISTING VUE FILE
      for (const skill of this.staffSkills) {
        if (this.skills.includes(skill)) {
          match++;
        }
      }
      return (match / this.skills.length) * 100;
    }
</script>

<template>
  <div>
    <!-- Apply for Role Modal -->
    <div
      id="authentication-modal"
      aria-hidden="true"
      class="inset-y-0 inset-x-0 hidden overflow-x-hidden overflow-y-auto bg-grey bg-opacity-75 fixed h-modal md:h-full top-4 left-0 right-0 md:inset-0 z-50 flex items-center justify-center"
    >
      <!-- Modal Content for "Apply for Role" -->
      <div class="relative pt-6 h-full w-11/12 md:h-auto w">
        <!-- ... Content for "Apply for Role" modal ... -->
        <!-- Modal content -->
          <div class="bg-white p-4 pb-0 rounded-lg shadow relative">
            <div class="bg-yellow w-full py-2 rounded-lg text-center">
              <span class="text-white text-lg">Confirm Details</span>
            </div>
            <div class="flex justify-end p-2">
              <button
                type="button"
                class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
                @click="closeModal"
              >
                <svg
                  class="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </button>
            </div>
            <div class="flex items-center justify-center -mt-6">
              <span class="font-serif text-lg">Apply Role</span>
            </div>
            <!-- form div here -->
            <div
              class="space-y-6 px-6 lg:px-8 pb-4 sm:pb-6 xl:pb-8 my-3"
              action="#"
            >
              <div class="bg-grey-50 px-4 py-6 md:px-8 my-3">
                <div class="grid grid-cols-3 pt-5 gap-6 md:gap-8">
                  <div>
                    <span class="font-bold pr-3">Staff ID:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 border-2 text-grey border-yellow rounded-md w-40"
                      :value="this.currentUser.staff_ID"
                      placeholder="1389503"
                      disabled
                    />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Department:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md w-64"
                      :value="this.currentUser.staff_dept"
                      placeholder="IT"
                      disabled
                    />
                  </div>
                  <div></div>
                </div>
                <!-- Second row of inputs -->
                <div class="grid grid-cols-3 pt-5 gap-6">
                  <div>
                    <span class="font-bold pr-3">First Name:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="this.currentUser.staff_FName"
                      disabled
                    />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Last Name:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="this.currentUser.staff_LName"
                      placeholder="Tam"
                      disabled
                    />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Email:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="this.currentUser.staff_email"
                      placeholder="email@123.com"
                      disabled
                    />
                  </div>
                </div>
                <!-- Third row of inputs  -->
                <div class="grid grid-cols-1 pt-5 gap-6 md:gap-8">
                  <span class="font-bold">Your Skills</span>
                  <div class="flex flex-col gap-2">
                    <label v-for="(skill, index) in staffSkills" :key="index">
                      <input
                        type="checkbox"
                        :name="skill"
                        :id="skill"
                        v-model="selectedSkills"
                        :value="skill"
                        disabled
                        checked
                      />
                      {{ skill }}
                    </label>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <button
                  @click="closeModal"
                  class="text-white bg-grey border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded-md text-md mr-3"
                >
                  Cancel
                </button>
                <button
                  @click="submitApplication"
                  class="text-white bg-yellow border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded-md text-md"
                >
                  Submit
                </button>
                <div
                  id="confirm-modal"
                  tabindex="-1"
                  class="fixed top-0 left-0 right-0 z-50 bg-grey bg-opacity-75 hidden w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full justify-center flex pt-24"
                >
                  <div class="relative w-full max-w-md max-h-full">
                    <!-- Modal content -->
                    <div
                      class="relative text-center bg-white rounded-lg shadow dark:bg-gray-700 w-full"
                    >
                      <!-- Modal header -->
                      <div
                        class="relative flex flex-col items-center justify-between rounded-t dark:border-gray-600 text-center"
                      >
                        <button
                          type="button"
                          class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ml-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                          @click="closeConfirm"
                        >
                          <svg
                            class="w-3 h-3"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 14 14"
                          >
                            <path
                              stroke="currentColor"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                            />
                          </svg>
                        </button>
                        <span v-if="applicationSuccess" class="text-green relative font-serif text-lg"
                          >Role Applied Successfully!</span
                        >
                        <span v-else class="text-red relative font-serif text-lg"
                          >Application Unsuccessful</span
                        >
                      </div>
                      <!-- Modal body -->
                      <div
                        class="p-6 space-y-6 flex flex-col justify-center items-center h-full"
                      >
                        <p
                          class="text-base leading-relaxed text-gray-500 dark:text-gray-400"
                        >
                          Thank you for your interest in the role!
                        </p>
                        <p v-if="applicationSuccess"
                          class="text-base leading-relaxed text-gray-500 dark:text-gray-400"
                        >
                          Your application is currently under review. <br />
                          We appreciate your patience and will be in touch soon.
                        </p>
                        <p v-else
                          class="text-base leading-relaxed text-gray-500 dark:text-gray-400"
                        >
                          There was an error with your application. You may only apply for a role once. If you think this is an error, please contact the Human Resource team.
                        </p>
                      </div>
                      <!-- Modal footer -->
                      <div
                        class="flex items-center space-x-2 border-gray-200 rounded-b dark:border-gray-600"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div
      id="confirm-modal"
      tabindex="-1"
      class="fixed top-0 left-0 right-0 z-50 bg-grey bg-opacity-75 hidden w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full justify-center flex pt-24"
    >
      <!-- Modal Content for Confirmation -->
      <div class="relative w-full max-w-md max-h-full">
        <!-- ... Content for Confirmation modal ... -->
      </div>
    </div>
  </div>
</template>