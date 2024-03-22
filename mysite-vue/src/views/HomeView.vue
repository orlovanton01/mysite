<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import { ref,onMounted,watch} from "vue"
  import {Course} from "@/api.js"
  // import { useSearchStore } from "@/stores/search.js"

  const props =defineProps(['search', 'data'])
  const ordering = ref('')
  const order = ref('')
  ordering.value='course_name'
  order.value='По возрастанию'
  const data =ref([])
  const min_price = ref('')
  const max_price = ref('')
  const min_training_period = ref('')
  const max_training_period = ref('')
  // let store=useSearchStore()
  // console.log(store)

  async function getData(){
    let filter
    if (order.value=='По возрастанию')
      filter ={ordering: ordering.value}
    else
      filter ={ordering: '-'+ordering.value}
    if (props.search){
      console.log(props.search)
      filter.search=props.search
    }
    if (min_price.value)
      filter.min_price=min_price.value
    if (max_price.value)
      filter.max_price=max_price.value
    if (min_training_period.value)
      filter.min_training_period=min_training_period.value
    if (max_training_period.value)
      filter.max_training_period=max_training_period.value
    // if (props.data){
    //   console.log(props.data)
    //   data.value=props.data
    // }
    // else
    data.value  = await Course.objects.filter(filter)
  }

  onMounted(()=>getData())
  watch(()=>props.search,()=>getData())
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

<template>
    <div class="row">
      <form class="col-3">
        <div class="sticky">
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
