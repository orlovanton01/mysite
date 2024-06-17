import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import axios from "axios"

// В роутере пишем перенаправления отрисовок для порта 5173
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      beforeEnter: (to, from, next) => {
        DisableUserEntry(to, from, next)
      },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegView.vue'),
      beforeEnter: (to, from, next) => {
        DisableUserEntry(to, from, next)
      },
    },
    {
      path: '/favourites',
      name: 'favourites',
      component: () => import('../views/FavView.vue'),
      beforeEnter: (to, from, next) => {
        DisableGuestEntry(to,from,next)
      },
    },
    {
      path: '/comparisons',
      name: 'comparisons',
      component: () => import('../views/ComView.vue'),
      beforeEnter: (to, from, next) => {
        DisableGuestEntry(to,from,next)
      },
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/Test.vue'),
      // beforeEnter: (to, from, next) => {
      //   DisableGuestEntry(to,from,next)
      // },
    },
    {
      path: '/modalmenu',
      name: 'modalmenu',
      component: () => import('../views/ModalMenu.vue'),
      // beforeEnter: (to, from, next) => {
      //   DisableGuestEntry(to,from,next)
      // },
    }
  ]
})

export default router


const DisableGuestEntry = function(to, from, next) {
  axios.get("/session/")
  .then(result=>{
    if (result.data.isAuthenticated){
      // Перенаправляем на избранное
      next()
    }
    else {
      // Перенаправляем на страницу входа
      next('login')
    }
  })
  .catch(error=>{
    // Ошибка при выполнении запроса
    return false
  })
};

const DisableUserEntry = function (to, from, next) {
  axios.get("/session/")
  .then(result=>{
    const IA = result.data.isAuthenticated
    if (IA){
      // Перенаправляем на домашнюю страницу
      next('')
    }
    else {
      // Перенаправляем на искомую страницу
      next()
    }
  })
  .catch(error=>{
    console.log("Ошибка при выполнении запроса")
    alert(error)
    return error
  })
};