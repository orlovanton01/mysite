import { shallowMount, mount, flushPromises } from '@vue/test-utils'
import {YOUR_V2_SITEKEY_HERE, YOUR_V3_SITEKEY_HERE} from '@/config'
import { createHead } from '@unhead/vue'
import { VueRecaptchaPlugin } from 'vue-recaptcha/head'
import { beforeEach, describe, vi  } from 'vitest'
import axios from 'axios'
import { when } from 'vitest-when'

import FavView from '@/views/FavView.vue'

vi.mock('axios')
when(axios.get).calledWith('/api/favourite/?user=1').thenReturn({
  data: [{"id":58,"course":{"id":732,"get_course_img_url":"/media/netology.png","owner":"netology","course_name":"1C-аналитик: с нуля до middle","price":"110100.00","final_rating":"0.0","link":"https://kurshub.ru/go/?id=52493","training_period":14},"user":1}]
})

describe('FavView.vue', () => {  
  let wrapper
  let vm
  beforeEach(async ()=>{
    // wrapper = shallowMount(FavView, {
    wrapper = mount(FavView, {
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
      await vm.Req()
      await vm.$nextTick()
    })

    it('Есть сообщение о загрузке/ошибке, нет курсов (Req + getData)', async()=> {
      expect(wrapper.find('[id="botMessage"]').exists()).toBe(true) // Есть сообщение о проерке капчи
      expect(wrapper.find('[id="guestMessage"]').exists()).toBe(false) // Нет сообщения об авторизации
      expect(wrapper.find('[class="card-body"]').exists()).toBe(false) // Нет курсов
    })

    it('Удаление из избранного: Не найдет курс', async()=> {
      expect(wrapper.find('[class="card-body"]').exists()).toBe(false) // Нет курсов
      expect(wrapper.find('[class="bi bi-trash"]').exists()).toBe(false) // Нет кнопки сохранения  
      expect(() => {wrapper.find('[class="bi bi-trash"]').trigger('click')}).toThrowError() // Не найдет кнопку чтобы нажать
    })
  })

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  describe('Гость',()=>{
    beforeEach(async()=>{
      when(axios.get).calledWith('/session/').thenResolve({
        data: {
          'isAuthenticated':false
        }
      })
      vm.human = true
      await vm.Req()
      await vm.$nextTick()
    })

    it('Есть сообщение о загрузке/ошибке, нет курсов (Req + getData)', async()=> {
      expect(wrapper.find('[id="botMessage"]').exists()).toBe(false) // Нет сообщения о проерке капчи
      expect(wrapper.find('[id="guestMessage"]').exists()).toBe(true) // Есть сообщение об авторизации
      expect(wrapper.find('[class="card-body"]').exists()).toBe(false) // Нет курсов
    })

    it('Удаление из избранного: Не найдет курс', async()=> {
      expect(wrapper.find('[class="card-body"]').exists()).toBe(false) // Нет курсов
      expect(wrapper.find('[class="bi bi-trash"]').exists()).toBe(false) // Нет кнопки сохранения  
      expect(() => {wrapper.find('[class="bi bi-trash"]').trigger('click')}).toThrowError() // Не найдет кнопку чтобы нажать
    })
  })
  
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
      await vm.Req()
      await vm.$nextTick()
    })

    it('Нет сообщения о загрузке/ошибке, Есть курсы (Req + getData)', async()=> {
      expect(wrapper.find('[id="botMessage"]').exists()).toBe(false) // Есть сообщение о проерке капчи
      expect(wrapper.find('[id="guestMessage"]').exists()).toBe(false) // Нет сообщения о авторизации
      expect(wrapper.find('[class="card-body"]').exists()).toBe(true) // Есть курсы
    })

    it('Удаление из избранного: Найдет, нажмет, отработает (DelFav)', async()=> {

      when(axios.delete).calledWith('/api/favourite/58/').thenResolve({})

      expect(wrapper.find('[class="card-body"]').exists()).toBe(true) // Есть курсы
      expect(wrapper.find('[class="bi bi-trash"]').exists()).toBe(true) // Есть кнопка сохранения

      const buySpy = vi.spyOn(vm, 'DelFav')
      expect(buySpy).not.toHaveBeenCalled()
      wrapper.find('[class="bi bi-trash"]').trigger('click')
      expect(buySpy).toHaveBeenCalled()
    })
  })  
})
