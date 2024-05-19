<script setup>
  import axios from "axios"
  import { ref,onMounted} from "vue"
  import {Fav} from "@/api.js"
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
        data.value = await Fav.objects.filter({user: userid.value})
      }
      // console.log(data.value)
    }

  async function DelFav(info){
    if (human.value == true){
      await axios.get("/session/")
      .then(result=>{
        if (result.data.isAuthenticated){
          console.log("Получен username")

          axios.delete(`/api/favourite/${info.id}/`)
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
    <h3>Избранное пользователя {{ username }}</h3>

    <div class="row" >
        <div class="col-12">
          <div class="row row-cols-1 row-cols-md-4 g-4">
              <div class="col" v-for="info in data">
                <div class="card h-100" style="width: 18rem; ">
                  <img :src="info.course.get_course_img_url" class="card-img-top" alt="Логотип школы">
                  <div class="card-body">
                    <h5 class="card-title">{{info.course.course_name}}<br></h5>
                    <h5 class="card-title">{{info.course.price}} ₽<br></h5>
                    <p class="card-text">{{info.course.training_period}} мес.</p>
                    <a :href='info.course.link' class="btn btn-primary">Перейти на сайт</a>
                    <a class="btn btn-outline-danger" @click="DelFav(info)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
        </div>
      </div>
    </div>
  </div>
</template>