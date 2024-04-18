import { shallowMount, mount, flushPromises } from '@vue/test-utils'
import {YOUR_V2_SITEKEY_HERE, YOUR_V3_SITEKEY_HERE} from '@/config'
import { createHead } from '@unhead/vue'
import { VueRecaptchaPlugin } from 'vue-recaptcha/head'
import { beforeEach, describe, vi  } from 'vitest'
import axios from 'axios'
import { when } from 'vitest-when'

import HomeView from '@/views/HomeView.vue'

vi.mock('axios')
when(axios.get).calledWith('/api/course/?ordering=course_name').thenReturn({
  data:[{"id":735,"get_course_img_url":"/media/netology.png","owner":"netology","course_name":"1C-аналитик","price":"100200.00","final_rating":"0.0","link":"https://kurshub.ru/go/?id=52481","training_period":9},{"id":732,"get_course_img_url":"/media/netology.png","owner":"netology","course_name":"1C-аналитик: с нуля до middle","price":"110100.00","final_rating":"0.0","link":"https://kurshub.ru/go/?id=52493","training_period":14},{"id":594,"get_course_img_url":"/media/netology.png","owner":"netology","course_name":"1С-программист","price":"90000.00","final_rating":"0.0","link":"https://kurshub.ru/go/?id=58778","training_period":11},{"id":626,"get_course_img_url":"/media/netology.png","owner":"netology","course_name":"1С-программист: первые шаги в профессию","price":"0.00","final_rating":"0.0","link":"https://kurshub.ru/go/?id=52356","training_period":5}]
})

describe('HomeView.vue', () => {  
  let wrapper
  let vm
  beforeEach(async ()=>{
    // wrapper = shallowMount(HomeView, {
    wrapper = mount(HomeView, {
      global: {
        plugins: [createHead(), [VueRecaptchaPlugin, {
          v2SiteKey: YOUR_V2_SITEKEY_HERE,
          v3SiteKey: YOUR_V3_SITEKEY_HERE,
      }]]
      }
    })
    await flushPromises()
    vm = wrapper.vm
  })

  describe('Бот',()=>{
    beforeEach(async()=>{
      when(axios.get).calledWith('/session/').thenResolve({
        data: {
          'isAuthenticated':false
        }
      })
      vm.human = false 
      await vm.getData()
      await vm.ShowStar()
      await vm.$nextTick()
    })

    it('Есть кнопка капчи, нет меню, нет курсов (getData)', async()=> {
      expect(wrapper.find('[class="btn btn-outline-danger"]').exists()).toBe(true) // Есть капча
      expect(wrapper.find('[class="form-control"]').exists()).toBe(false) // Нет меню
      expect(wrapper.find('[class="card-body"]').exists()).toBe(false) // Нет курсов
    })

    it('Добавление в избранное: Не найдет курс', async()=> {
      expect(wrapper.find('[class="card-body"]').exists()).toBe(false) // Нет курсов
      expect(wrapper.find('[class="bi bi-star"]').exists()).toBe(false) // Нет кнопки сохранения  
      expect(() => {wrapper.find('[class="bi bi-star"]').trigger('click')}).toThrowError() // Не найдет кнопку чтобы нажать
    })
  })

  describe('Гость',()=>{
    beforeEach(async ()=>{
      when(axios.get).calledWith('/session/').thenResolve({
        data: {
          'isAuthenticated':false
        }
      })
      vm.human = true 
      await vm.getData()
      await vm.ShowStar()
      await vm.$nextTick()
    })

    it('Нет кнопки капчи, есть меню, есть курсы, нет кнопки сохранения (getData + ShowStar)', async()=> {
      expect(wrapper.find('[class="btn btn-outline-danger"]').exists()).toBe(false) // Нет капчи
      expect(wrapper.find('[class="form-control"]').exists()).toBe(true) // Есть меню
      expect(wrapper.find('[class="card-body"]').exists()).toBe(true) // Есть курсы
      expect(wrapper.find('[class="bi bi-star"]').exists()).toBe(false) // Нет кнопки сохранения
    })

    it('Добавление в избранное: Не найдет кнопку', async()=> {
      expect(wrapper.find('[class="card-body"]').exists()).toBe(true) // Есть курсы
      expect(wrapper.find('[class="bi bi-star"]').exists()).toBe(false) // Нет кнопки сохранения  
      expect(() => {wrapper.find('[class="bi bi-star"]').trigger('click')}).toThrowError() // Не найдет кнопку чтобы нажать
    })
  })
  
  describe('Пользователь',()=>{
    beforeEach(async ()=>{
      when(axios.get).calledWith('/session/').thenResolve({
        data: {
          'isAuthenticated': true,
          'username': 'TestUser',
          'id': 1
        }
      })
      vm.human = true 
      await vm.getData()
      await vm.ShowStar()
      await vm.$nextTick()
    })

    it('Нет кнопки капчи, есть меню, есть курсы, есть кнопка сохранения (getData + ShowStar)', async()=> {
      expect(wrapper.find('[class="btn btn-outline-danger"]').exists()).toBe(false) // Нет капчи
      expect(wrapper.find('[class="form-control"]').exists()).toBe(true) // Есть меню
      expect(wrapper.find('[class="card-body"]').exists()).toBe(true) // Есть курсы
      expect(wrapper.find('[class="bi bi-star"]').exists()).toBe(true) // Есть кнопка сохранения
    })

    it('Добавление в избранное: Найдет, нажмет, отработает (AddFav)', async()=> {
      expect(wrapper.find('[class="card-body"]').exists()).toBe(true) // Есть курсы
      expect(wrapper.find('[class="bi bi-star"]').exists()).toBe(true) // Есть кнопка сохранения

      const buySpy = vi.spyOn(vm, 'AddFav')
      expect(buySpy).not.toHaveBeenCalled()
      wrapper.find('[class="bi bi-star"]').trigger('click')
      expect(buySpy).toHaveBeenCalled()
    })
  })  
})
