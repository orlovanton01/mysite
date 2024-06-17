<script setup>
  import axios from "axios"
  import { ref,onMounted} from "vue"
  import {Com} from "@/api.js"
  import { useRecaptchaProvider } from 'vue-recaptcha'
  import { useChallengeV3 } from 'vue-recaptcha'

  const data =ref([])
  let username = ref('') 
  let userid = ref('')
  const human = ref(false)

  onMounted(()=> onSubmit())
  
  async function Req() {
    if (human.value == true){
      await axios.get("/session/")
      .then(result=>{
        if (result.data.isAuthenticated){
          username.value = result.data.username
          userid.value = result.data.id
          getData()
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

  async function getData(){
      // console.log("PreFilter")
      if (human.value == true){
        data.value = await Com.objects.filter({user: userid.value})
      }
      // console.log(data.value)
    }

  async function DelCom(info){
    if (human.value == true){
      await axios.get("/session/")
      .then(result=>{
        if (result.data.isAuthenticated){
          console.log("Получен username")

          axios.delete(`/api/comparison/${info.id}/`)
          .then(()=>getData())
          console.log("Подчистил")
        }
      })
      .catch(error=>{
        console.log("Ошибка при выполнении запроса")
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
      Req()
    })
  }
</script>

<template>
  <div id="botMessage" v-if="human==false"><h3>Проверяем reCaptcha...</h3></div>
  <div id="guestMessage" v-else-if="username==''"><h3>Вы не авторизованы</h3></div>
  <!-- <div v-if="human == true, username!=''"> -->
  <div v-else>
    <strong>Если вы видите эту страницу, то вы авторизованы</strong>
    <h3>Сравнения пользователя {{ username }}</h3>
      <div class="cont">
        <!-- <table class="table">
            <thead>
                <tr>
                    <th scope="col">Название курса</th>
                    <th scope="col">Платформа</th>
                    <th scope="col">Цена, ₽</th>
                    <th scope="col">Время обучения, мес.</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="info in data">
                    <th scope="row"><a :href='info.course.link' class="link">{{info.course.course_name}}</a></th>
                    <td><img :src="info.course.get_course_img_url" class="card-img-top" alt="Логотип школы"></td>
                    <td>{{info.course.price}}</td>
                    <td>{{info.course.training_period}}</td>
                    <td>
                        <a class="btn btn-outline-danger" @click="DelCom(info)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                            </svg>
                        </a>
                    </td>
                </tr>
            </tbody>
        </table> -->
        
        <table class="table">
          <thead>
            <tr>
              <th>Название курса</th>
              <th scope="col" v-for="info in data">
                <a :href='info.course.link' class="link">{{info.course.course_name}}</a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Платформа</th>
              <td v-for="info in data">
                {{info.course.owner}}
              </td>
            </tr>
            <tr>
              <th scope="row">Цена, ₽</th>
              <td v-for="info in data">
                {{info.course.price}}
              </td>
            </tr>
            <tr>
              <th scope="row">Время обучения, мес.</th>
              <td v-for="info in data">
                {{info.course.training_period}}
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <th scope="row"></th>
              <td v-for="info in data">
                <a class="btn btn-outline-danger" @click="DelCom(info)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                    </svg>
                </a>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
</template>

<style scoped>
    .link{
        text-decoration: none;
        color: black;
    }
    .th, .td, .tr{
        text-align: center;
        vertical-align: center;
    }
    .cont{
        overflow-x: auto;
        position: relative;
    }
    .table{
      position: relative;
      border-collapse: collapse;
    }
    thead th{
      position: sticky;
      top: 0;
    }
    thead th:first-child {
      left: 0;
      z-index: 1;
    }
    tbody th{
      position: sticky;
      left: 0;
    }
    tfoot th {
      position: sticky;
      bottom: 0;
    }
    tfoot th:first-child {
      left: 0;
      z-index: 1;
    }
</style>