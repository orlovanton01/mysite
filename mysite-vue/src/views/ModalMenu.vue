<script setup lang="ts">
import { ModalsContainer, useModal } from 'vue-final-modal'
import ModalConfirm from '@/views/Test.vue'

import { ref,onMounted} from "vue"
  import axios from "axios"
  import {Fav} from "@/api.js"
  import { useRecaptchaProvider } from 'vue-recaptcha'
  import { useChallengeV3 } from 'vue-recaptcha'
  
  const data =ref([])
  let username = ref('') 
  let userid = ref('')
  const human = ref(false)

const { open, close, patchOptions } = useModal({
  component: ModalConfirm,
  attrs: {
    title: 'Hello World!',
    onConfirm() {
      close()
    },
  },
  slots: {
    default: '<p>UseModal: The content of the modal</p> <h1>Hmmm?</h1>',
    "user": username
  },
})

  

  onMounted(()=> onSubmit())

  async function onSubmit() {
    const response = await execute()
    // do something with response
    axios.post('/api/verify-captcha/',{
      "token": response,
      "version" : "V3",
    })
    .then(result => {
      console.log(result.data.is_human)
      human.value = result.data.is_human
      Req()
    })
  }

  async function Req() {
    if (human.value == true){
      await axios.get("/session/")
      .then(result=>{
        console.log(result.data)
        if (result.data.isAuthenticated){
          username.value = result.data.username
          userid.value = result.data.id
          patchOptions({
            attrs: {
              // Overwrite the modal's props
              user : username.value
            }
          })
        }
        else {
          username.value = ""
        }
      })
      .catch(error=>{
        console.log("Ошибка при выполнении запроса")
        username.value = error.data.response
      })
    }
  }

  useRecaptchaProvider()
  const { execute } = useChallengeV3('submit')

</script>

<template>
  <p>User is {{ username }}</p>
  <button @click="() => open()">
    Open Modal
  </button>

  <ModalsContainer />
</template>