<script setup>
import axios from "axios"
  import { ref,onMounted} from "vue"

  const data =ref([])
  let username = ref('') 


  onMounted(()=> Req())
  
  async function Req() {
    await axios.get("/session/")
    .then(result=>{
      if (result.data.isAuthenticated){
        axios.get("/whoami/")
        .then((result)=>{
          username.value = result.data.username
        })
      }
      else {
        username.value = "Гость"
      }
    })
    .catch(error=>{
      console.log("Ошибка при выполнении запроса")
      username.value = error.data.response
    })
  }

  async function Logout(){
    axios.post("/logout/", {
    },)
    .then(response=>{
      window.location.replace('/')
    })
    .catch(error => {
      console.log(error.response)
      alert(error)
    })
  }
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container">
        <a class="navbar-brand" href="/">Агрегатор</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Переключатель навигации">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="/">Главная</a>
            </li>
            <!-- <li class="nav-item dropdown" v-if="username == 'Гость'">
              <a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Войти
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/login">Вход</a></li>
                <li><a class="dropdown-item" href="#">Регистрация</a></li>
              </ul>
            </li>
            <li class="nav-item" v-else><a class="nav-link active" href="" @click="Logout">Выйти</a></li> -->
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Сравнение</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="/favourites">Избранное</a>
            </li>
          </ul>
          <div class="d-flex">
            Вы авторизованы как: {{ username }}
          </div>
          <ul class="navbar-nav">
            <li class="nav-item fst-italic fw-bold" v-if="username == 'Гость'"><a class="nav-link active" href="/login">Вход</a></li>
            <li class="nav-item fst-italic fw-bold" v-if="username == 'Гость'"><a class="nav-link active" href="/register">Регистрация</a></li>
            <li class="nav-item fst-italic fw-bold" v-else><a class="nav-link active" href="" @click="Logout">Выйти</a></li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container" id="main">
      <RouterView />
  </div>
</template>

<style>
#main{
  padding-top: 2%;
}
*{
  font-size:14px;
}
</style>
