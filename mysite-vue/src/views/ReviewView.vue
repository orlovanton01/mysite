  <script setup lang="ts">
  import { VueFinalModal } from 'vue-final-modal'
  import { ref,onMounted} from "vue"
  import axios from "axios"
  import {Fav} from "@/api.js"
  import { useRecaptchaProvider } from 'vue-recaptcha'
  import { useChallengeV3 } from 'vue-recaptcha'
  
  const data =ref([])
  let username = ref('') 
  let userid = ref('')
  const human = ref(false)

  defineProps<{
    user?: string
    name?: string
    id?: string
  }>()

  const emit = defineEmits<{
    (e: 'confirm'): void
  }>()
  
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
    <VueFinalModal
      class="confirm-modal"
      content-class="confirm-modal-content"
      overlay-transition="vfm-fade"
      content-transition="vfm-fade"
    >
    <div id="botMessage" v-if="human==false"><h3>Проверяем reCaptcha...</h3></div>
    <div id="guestMessage" v-else-if="username==''"><h3>Вы не авторизованы</h3></div>
    <!-- <div v-if="human == true, username!=''"> -->
    <div v-else>
        Вы авторизованы как {{ user }}
        <h1>Отзывы к курсу "{{ name }}"</h1>
        <i>Идентификатор курса - {{ id }}</i>
        <slot /> 

        <br>
        <button @click="emit('confirm')">
            Confirm
        </button> 
    </div>
      
    </VueFinalModal>
  </template>

  <style>
  .confirm-modal {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .confirm-modal-content {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background: #fff;
    border-radius: 0.5rem;
  }
  .confirm-modal-content > * + *{
    margin: 0.5rem 0;
  }
  .confirm-modal-content h1 {
    font-size: 1.375rem;
  }
  .confirm-modal-content button {
    margin: 0.25rem 0 0 auto;
    padding: 0 8px;
    border: 1px solid;
    border-radius: 0.5rem;
  }
  .dark .confirm-modal-content {
    background: #000;
  }
  </style>
