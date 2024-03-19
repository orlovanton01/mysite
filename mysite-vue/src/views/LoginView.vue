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

          <form>
            <!-- Email input -->
            <div class="form-outline mb-4">
              <input id="form2Example1" class="form-control" v-model="login" type="text" placeholder="Логин"/>
              <label class="form-label" for="form2Example1">Логин</label>
            </div>

            <!-- Password input -->
            <div class="form-outline mb-4">
              <input id="form2Example2" class="form-control" v-model="password" type="password" placeholder="Пароль"/>
              <label class="form-label" for="form2Example2">Пароль</label>
            </div>

            
            <!-- <div class="row mb-4">
              <div class="col d-flex justify-content-center">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="form2Example31" checked />
                  <label class="form-check-label" for="form2Example31"> Remember me </label>
                </div>
              </div>

              <div class="col">
                <a href="#!">Forgot password?</a>
              </div>
            </div> -->

            <!-- Submit button -->
            <a class="btn btn-primary btn-block mb-4" @click="setLogin">Войти</a>

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

<script>
  import $ from 'jquery'
  export default {
      name: "Login",
      data() {
          return {
              login: '',
              password: '',
          }
      },
      methods: {
          setLogin() {
              $.ajax({
                  url: "http://localhost:8000/token/",
                  // "http://localhost:8000/token/" СРАБОТАЛ
                  type: "POST",
                  data: {
                      username: this.login,
                      password: this.password
                  },
                  success: (response) => {
                      
                      console.log(response)
                      localStorage.setItem("auth_token", response.token)
                      // this.$router.push({name: "/"})
                      alert("Спасибо что Вы с нами")
                  },
                  error: (response) => {
                      if (response.status === 400) {
                          alert("Логин или пароль не верен")
                      }
                      else{
                        console.log(response)
                        alert(response)
                      }
                  }
              })
          },
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