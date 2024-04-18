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
              <h3 class="form-label fst-italic fw-bold">Авторизация</h3>
            </div>

            <!-- Login input -->
            <div class="form-outline mb-4">
              <input id="form2Example1" class="form-control" v-model="login" type="text" placeholder="Username"/>
              <label class="form-label" for="form2Example1">Логин</label>
            </div>

            <!-- Password input -->
            <div class="form-outline mb-4">
              <input id="form2Example2" class="form-control" v-model="password" type="password" placeholder="Password"/>
              <label class="form-label" for="form2Example2">Пароль</label>
            </div>

            <!-- Submit button -->
            <a type="submit button" class="btn btn-primary btn-block mb-4"  @click="setLogin()" >Войти</a>

          </form>

        </div>
      </div>
    </div>
  </div>
</section>
</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted,watch } from "vue"
  import { useRecaptchaProvider } from 'vue-recaptcha'
  import { useChallengeV3 } from 'vue-recaptcha'
  
  const human = ref(false)
  const auth = ref(true)

  const login = ref('')
  const password = ref('')

  onMounted(()=>onSubmit())

  async function setLogin(){
    if (human.value == true, auth.value == false){
      axios.post("/loginuser/", {
        username: login.value,
        password: password.value
      })
      .then(response=>{
        console.log("Авторизовался")
        window.location.replace('/')  
      })
      .catch(error => {
        if (error.response.status === 400) {
          alert("Логин или пароль не верен, убедитесь в правильности введенных данных")
        }
        else{
          console.log(error.response)
          alert(error)
        }
      })
    }
    
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