<script setup>
  import { ref,onMounted,watch} from "vue"
  import {Course} from "@/api.js"

  const ordering = ref('')
  const order = ref('')
  ordering.value='course_name'
  order.value='По возрастанию'
  const data =ref([])
  const min_price = ref('')
  const max_price = ref('')
  const min_training_period = ref('')
  const max_training_period = ref('')
  const search = ref("")

  async function getData(){
    let filter
    if (order.value=='По возрастанию')
      filter ={ordering: ordering.value}
    else
      filter ={ordering: '-'+ordering.value}
    if (search.value)
      filter.search=search.value
    if (min_price.value)
      filter.min_price=min_price.value
    if (max_price.value)
      filter.max_price=max_price.value
    if (min_training_period.value)
      filter.min_training_period=min_training_period.value
    if (max_training_period.value)
      filter.max_training_period=max_training_period.value
    data.value  = await Course.objects.filter(filter)
    // console.log(await Course.objects.filter(filter))
    // console.log(data.value)
  }

  onMounted(()=>getData())
  watch(()=>search.value,()=>getData())
  watch(()=>ordering.value,()=>getData())
  watch(()=>order.value,()=>getData())
  watch(()=>min_price.value,()=>getData())
  watch(()=>max_price.value,()=>getData())
  watch(()=>min_training_period.value,()=>getData())
  watch(()=>max_training_period.value,()=>getData())

  function reset(){
    search.value=''
    order.value=''
    ordering.value=''
    min_price.value=''
    max_price.value=''
    min_training_period.value=''
    max_training_period.value=''
  }


  import axios from "axios"
  async function AddFav(info){
    await axios.get("/session/")
    .then(result=>{
      if (result.data.isAuthenticated){
        console.log("Авторизован, загружаю курсы")
        axios.get("/whoami/")
        .then((result)=>{
          console.log("Получен username")
          axios.post("/api/favourite/", {
            "user" : result.data.id,
            "course" : info.id,
          })
        })
      }
      else {
        console.log("Нужно войти")
      }
    })
    .catch(error=>{
      console.log("Ошибка при выполнении запроса")
    })
  }
</script>

<template>
    <div class="row">
      <form class="col-3">
        <div class="sticky">
          <div class="mb-3">
            <input v-model="search" class="form-control me-2" type="search" placeholder="Поиск" aria-label="Поиск">
          </div>
          <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Сортировать</label>
            <div class="input-group">
              <select class="form-select" v-model="ordering">
                <option value="course_name">По названию</option>
                <option value="price">По стоимости</option>
                <option value="training_period">По сроку обучения</option>
              </select>
              <select class="form-select" v-model="order">
                <option value="По возрастанию">По возрастанию</option>
                <option value="По убыванию">По убыванию</option>
              </select>
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleFormControlInput12" class="form-label">Цена</label>
            <div class="input-group">
              <input type="number" class="form-control" id="exampleFormControlInput2" placeholder="От, ₽" v-model="min_price">
              <input type="number" class="form-control" id="exampleFormControlInput2" placeholder="До, ₽" v-model="max_price">
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleFormControlInput3" class="form-label">Продолжительность обучения</label>
            <div class="input-group">
              <input type="number" class="form-control" id="exampleFormControlInput3" placeholder="От, мес." v-model="min_training_period">
              <input type="number" class="form-control" id="exampleFormControlInput3" placeholder="До, мес." v-model="max_training_period">
            </div>
          </div>
          <a type="submit" class="btn btn-danger" @click="reset">Сбросить</a>
        </div>
      </form>
      <div class="col-9">
        <div class="row row-cols-1 row-cols-md-3 g-4">
            <div class="col" v-for="course in data">
              <div class="card h-100" style="width: 18rem; ">
                <img :src="course.get_course_img_url" class="card-img-top" alt="Логотип школы">
                <div class="card-body">
                  <h5 class="card-title">{{course.course_name}}<br></h5>
                  <h5 class="card-title">{{course.price}} ₽<br></h5>
                  <p class="card-text">{{course.training_period}} мес.</p>
                  <a href='{{course.link}}' class="btn btn-primary">Перейти на сайт</a>
                  <a class="btn btn-outline-warning" @click="AddFav(course)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-star" viewBox="0 1 16 16">
                      <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"/>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
      </div>
    </div>
  </div>
</template>

<style>
  .sticky{
      position: sticky; 
      top: 0;
  }
</style>
