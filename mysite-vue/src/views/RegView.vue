<template>
  <section class=" text-center text-lg-start">
  <div class="card mb-3">
    <div class="row g-0 d-flex align-items-center">
      <div class="col-lg-4 d-none d-lg-flex">
        <img src="../../../media/kursy.jpg" alt="Программирование"
          class="w-100 rounded-t-5 rounded-tr-lg-0 rounded-bl-lg-5" />
      </div>
      <div class="col-lg-8">
        <div class="card-body py-5 px-md-5">
          <div id="botMessage" v-if="human==false"><h3>Проверяем reCaptcha...</h3></div>
          <div id="loggedMessage" v-else-if="auth==true"><h3>Вы уже авторизованы</h3></div>
          <form class="EntryForm" v-else>

            <div class="form-outline mb-4">
              <h3 class="form-label fst-italic fw-bold">Регистрация</h3>
            </div>

            <!-- Login input -->
            <div class="form-outline mb-4">
              <input id="form2Example1" class="form-control" v-model="login" type="text" placeholder="Username"/>
              <label class="form-label" for="form2Example1">Логин</label>
            </div>

            <!-- Password input -->
            <div class="form-outline mb-4">
              <input id="form2Example2" class="form-control" v-model="password1" type="password" placeholder="Password"/>
              <label class="form-label" for="form2Example2">Пароль</label>
              <input id="form2Example3" class="form-control" v-model="password2" type="password" placeholder="Confirm password"/>
              <label class="form-label" for="form2Example2">Повторите пароль</label>
            </div>

            <!-- Submit button -->
            <a class="btn btn-primary btn-block mb-4" @click="setLogin()" >Войти</a>

          </form>

        </div>
      </div>
    </div>
  </div>
</section>
  <!-- <div>
      <input v-model="login" type="text" placeholder="Логин"/>
      <input v-model="password" type="password" placeholder="Пароль"/>
      <button @click="setLogin">Войти</button>
  </div> -->
</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted,watch} from "vue"
  import { useRecaptchaProvider } from 'vue-recaptcha'
  import { useChallengeV3 } from 'vue-recaptcha'
  
  const login = ref('')
  const password1 = ref('')
  const password2 = ref('')
  const human = ref(false)
  const auth = ref(true)

  onMounted(()=>onSubmit())

  async function setLogin(){
    axios.post("/registeruser/", {
      // withcredentials: true,
      username: login.value,
      password1: password1.value,
      password2: password2.value,
    })
    .then(response=>{
      console.log('Зарегал')
      window.location.replace('/')
    })
    .catch(error => {
      if (error.response.status === 400) {
        alert("Убедитесь в правильности введенных данных: \n" + error.response.data.errors.join("\n"))
      }
      else{
        console.log(error.response)
        alert(error)
      }
    })
  }

  useRecaptchaProvider()
  const { execute } = useChallengeV3('submit')

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
      checkSession()
    })
  }

  async function checkSession() {
    if (human.value == true){
      await axios.get("/session/")
      .then(result=>{
        auth.value = result.data.isAuthenticated
      })
      .catch(error=>{
        console.log("Ошибка при выполнении запроса")
        auth.value = true
      })
    } 
  }
</script>

<style>
    .rounded-t-5 {
      border-top-left-radius: 0.5rem;
      border-top-right-radius: 0.5rem;
    }

    @media (min-width: 992px) {
      .rounded-tr-lg-0 {
        border-top-right-radius: 0;
      }

      .rounded-bl-lg-5 {
        border-bottom-left-radius: 0.5rem;
      }
    }
  </style>