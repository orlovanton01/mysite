<template>
  <strong>Если вы видите эту страницу то вы авторизованы. В дальнейшем здесь будут находиться сохраненные в избранное крусы</strong>
  <h3>Избранное пользователя {{ username }}</h3>

  <div class="row">
      <div class="col-12">
        <div class="row row-cols-1 row-cols-md-4 g-4">
            <div class="col" v-for="course in data">
              <div class="card h-100" style="width: 18rem; ">
                <img :src="course.get_course_img_url" class="card-img-top" alt="Логотип школы">
                <div class="card-body">
                  <h5 class="card-title">{{course.course_name}}<br></h5>
                  <h5 class="card-title">{{course.price}} ₽<br></h5>
                  <p class="card-text">{{course.training_period}} мес.</p>
                  <a href='{{course.link}}' class="btn btn-primary">Перейти на сайт</a>
                </div>
              </div>
            </div>
      </div>
    </div>
  </div>

</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted,watch} from "vue"
  onMounted(()=> Req())
  
  let username = ref('') 

  async function Req() {
    await axios.get("/session/")
        .then(result=>{
          if (result.data.isAuthenticated){
            console.log("Авторизован, загружаю курсы")
            axios.get("/whoami/")
            .then((result)=>{
              console.log("Получен username")
              username.value = result.data.username
            })
          }
          else {
            console.log("Нужно войти")
            username.value = "Anon"
          }
        })
        .catch(error=>{
          console.log("Ошибка при выполнении запроса")
          username.value = error
        })
  }

  import {Course} from "@/api.js"

  const props =defineProps(['data'])
  console.log(props.data)
  const ordering = ref('')
  const order = ref('')
  ordering.value='course_name'
  order.value='По возрастанию'
  const data =ref([])
  const min_price = ref('')
  const max_price = ref('')
  const min_training_period = ref('')
  const max_training_period = ref('')

  async function getData(){
    let filter
    if (order.value=='По возрастанию')
      filter ={ordering: ordering.value}
    else
      filter ={ordering: '-'+ordering.value}
    if (min_price.value)
      filter.min_price=min_price.value
    if (max_price.value)
      filter.max_price=max_price.value
    if (min_training_period.value)
      filter.min_training_period=min_training_period.value
    if (max_training_period.value)
      filter.max_training_period=max_training_period.value
    data.value  = await Course.objects.filter(filter)
  }

  onMounted(()=>getData())
  watch(()=>props.data,()=>getData())
  watch(()=>ordering.value,()=>getData())
  watch(()=>order.value,()=>getData())
  watch(()=>min_price.value,()=>getData())
  watch(()=>max_price.value,()=>getData())
  watch(()=>min_training_period.value,()=>getData())
  watch(()=>max_training_period.value,()=>getData())

  function reset(){
    order.value=''
    ordering.value=''
    min_price.value=''
    max_price.value=''
    min_training_period.value=''
    max_training_period.value=''
  }

</script>