import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import axios from "axios"
axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


import { VueRecaptchaPlugin } from 'vue-recaptcha/head'





const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueRecaptchaPlugin, {
    v2SiteKey: '6LchCrMpAAAAAJhHAvgrfHTOZu-Qh4omd_pN8f5e',
    v3SiteKey: '6LfxELMpAAAAAITRlY3SlD6HyZcB6TN3p4hpsWv9',
})

app.mount('#app')