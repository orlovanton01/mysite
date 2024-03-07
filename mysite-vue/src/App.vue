<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { ref,onMounted} from "vue"
import {Course} from "@/api.js"

const search = ref("")
const data =ref([])
  async function getData(){
      data.value   = await Course.objects.filter({name:search.value})
  }
  onMounted(()=>getData())
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container">
        <a class="navbar-brand" href="#">Агрегатор</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Переключатель навигации">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Главная</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Войти
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Вход</a></li>
                <li><a class="dropdown-item" href="#">Регистрация</a></li>
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Сравнение</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Избранное</a>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input v-model="search" @input="getData" class="form-control me-2" type="search" placeholder="Поиск" aria-label="Поиск">
            <button class="btn btn-outline-success" type="submit">Поиск</button>
          </form>
        </div>
      </div>
    </nav>
    <div class="container">
      <RouterView />
  </div>
</template>

<style scoped>
</style>
