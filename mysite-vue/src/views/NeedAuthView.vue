<template>
  <strong>Для доступа к избранному вам необходимо авторизоваться</strong>
</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted,watch} from "vue"
  onMounted(()=>Req())

  async function Req(){
    axios.get("/whoami/")
    .then(result=>{
      // console.log("Страница перенаправления на логин")
      // console.log(result.data)
      })
  }
</script>