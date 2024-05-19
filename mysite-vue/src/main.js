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


// import { VueRecaptchaPlugin } from 'vue-recaptcha/head'
import {YOUR_V2_SITEKEY_HERE, YOUR_V3_SITEKEY_HERE} from './config'
import { createHead } from '@unhead/vue'
import { VueRecaptchaPlugin } from 'vue-recaptcha'




const app = createApp(App)

// app.use(createPinia())
app.use(router)
const head = createHead()
app.use(head)
app.use(VueRecaptchaPlugin, {
    v2SiteKey: YOUR_V2_SITEKEY_HERE,
    v3SiteKey: YOUR_V3_SITEKEY_HERE,
})

app.mount('#app')

document.title = 'Агрегатор курсов'