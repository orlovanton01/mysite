import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import axios from "axios"

// В роутере пишем перенаправления отрисовок для порта 5173
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/favourites',
      name: 'favourites',
      component: () => import('../views/FavView.vue'),
      beforeEnter: (to, from, next) => {
        IsAuth(to,from,next)
      },
    },
    {
      path: '/needauth',
      name: 'needauth',
      component: () => import('../views/NeedAuthView.vue'),
    }
  ]
})

export default router


const IsAuth = function(to, from, next) {
  axios.get("/session/")
        .then(result=>{
          if (result.data.isAuthenticated){
            console.log("Перенаправляем на избранное")
            next()
          }
          else {
            console.log("Перенаправляем на страницу ошибки")
            next('needauth')
          }
        })
        .catch(error=>{
          console.log("Ошибка при выполнении запроса")
          return false
        })
};