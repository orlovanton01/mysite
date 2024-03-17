<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import { ref,onMounted,watch} from "vue"
  import {Course} from "@/api.js"

  const props =defineProps(['search'])
  console.log(props.search)
  const ordering = ref('')
  const data =ref([])

  async function getData(){
    let filter ={ordering: 'course_name'}
    data.value  = await Course.objects.filter(filter)
  }
  
  function setOrdering(field, order){
    console.log(field, order)
    if (order=='По возрастанию')
      ordering.value=field
    else 
      ordering.value='-'+field  
  }
  onMounted(()=>getData())
  // onMounted(()=>setOrdering('course_name', 'По возрастанию'))
  watch(()=>props.search,()=>getData())
</script>

<template>
    <div class="row">
      <form class="col-3">
        <div class="sticky">
          <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Сортировать</label>
            <div class="input-group">
              <select class="form-select" id="field">
                <option value="По названию">По названию</option>
                <option value="По стоимости">По стоимости</option>
                <option value="По сроку обучения">По сроку обучения</option>
              </select>
              <select class="form-select" id="order">
                <option value="По возрастанию">По возрастанию</option>
                <option value="По убыванию">По убыванию</option>
              </select>
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleFormControlInput12" class="form-label">Цена</label>
            <div class="input-group">
              <input type="number" class="form-control" id="exampleFormControlInput2" placeholder="От, ₽">
              <input type="number" class="form-control" id="exampleFormControlInput2" placeholder="До, ₽">
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleFormControlInput3" class="form-label">Продолжительность обучения</label>
            <div class="input-group">
              <input type="number" class="form-control" id="exampleFormControlInput3" placeholder="От, мес.">
              <input type="number" class="form-control" id="exampleFormControlInput3" placeholder="До, мес.">
            </div>
          </div>
          <a type="submit" class="btn btn-success" @click="setOrdering(document.getElementById('field').value, document.getElementById('order').value)">Применить</a>
          <a type="submit" class="btn btn-danger">Сбросить</a>
        </div>
      </form>
      <div class="col-9" v-if="data">
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
      </div v-else>
      <p>No courses are available.</p>
    </div>
  </div>
</template>

<style>
  .sticky{
      position: sticky; 
      top: 0;
  }
</style>
