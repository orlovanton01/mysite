<template>
  <strong>Хоба, это страница с избранным</strong>
</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted,watch} from "vue"
  onMounted(()=>Req())

  async function Req(){
    axios.get("/whoami/")
    .then(result=>{
      console.log(result)
      })
  }
</script>