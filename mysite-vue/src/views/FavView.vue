<template>
  <strong>Если вы видите эту страницу то вы авторизованы. В дальнейшем здесь будут находиться сохраненные в избранное крусы</strong>
</template>

<script setup>
  import axios from "axios"
  import { ref,onMounted,watch} from "vue"
  onMounted(()=>Req())

  async function Req(){
    axios.get("/whoami/")
    .then(result=>{
      // console.log("ниже setup request")
      // console.log(result.data)
    })
  }
</script>