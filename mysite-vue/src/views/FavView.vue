<template>
  <strong>Если вы видите эту страницу то вы авторизованы. В дальнейшем здесь будут находиться сохраненные в избранное курсы</strong>
  <h3>Избранное пользователя {{ username }}</h3>

  <div class="row">
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

</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted} from "vue"
  import {Fav} from "@/api.js"

  const data =ref([])
  let username = ref('') 
  let userid = ref('')

  onMounted(()=> Req())
  
  async function Req() {
    await axios.get("/session/")
    .then(result=>{
      if (result.data.isAuthenticated){
        axios.get("/whoami/")
        .then((result)=>{
          username.value = result.data.username
          userid.value = result.data.id
          getData()
        })
      }
      else {
        username.value = "Anon"
      }
    })
    .catch(error=>{
      console.log("Ошибка при выполнении запроса")
      username.value = error.data.response
    })
  }

  async function getData(){
      // console.log("PreFilter")
      data.value = await Fav.objects.filter({user: userid.value})
      // console.log(data.value)
    }

  async function DelFav(info){
    await axios.get("/session/")
    .then(result=>{
      if (result.data.isAuthenticated){
        axios.get("/whoami/")
        .then((result)=>{
          console.log("Получен username")

          axios.delete(`/api/favourite/${info.id}/`)
          .then(()=>getData())
        })
      }
    })
    .catch(error=>{
      console.log("Ошибка при выполнении запроса")
    })
  }

</script>