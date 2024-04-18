import { shallowMount, mount, flushPromises } from '@vue/test-utils'
import {YOUR_V2_SITEKEY_HERE, YOUR_V3_SITEKEY_HERE} from '@/config'
import { createHead } from '@unhead/vue'
import { VueRecaptchaPlugin } from 'vue-recaptcha/head'
import { beforeEach, describe, vi  } from 'vitest'
import axios from 'axios'
import { when } from 'vitest-when'

import RegView from '@/views/RegView.vue'

vi.mock('axios')

describe('RegView.vue', () => {  
  let wrapper
  let vm
  beforeEach(async ()=>{
    // wrapper = shallowMount(RegView, {
    wrapper = mount(RegView, {
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
      await vm.checkSession()
      await vm.$nextTick()
    })

    it('Бесконечное сообщение проверки капчи', async()=> {
      expect(wrapper.find('[id="botMessage"]').exists()).toBe(true) // Есть сообщение о проерке капчи
      expect(wrapper.find('[id="loggedMessage"]').exists()).toBe(false) // Нет сообщения об авторизации
      expect(wrapper.find('[class="EntryForm"]').exists()).toBe(false) // Нет курсов
    })

    it('Не найдет кнопку входа и не сможет нажать', async()=> {
      expect(wrapper.find('[class="EntryForm"]').exists()).toBe(false) // Нет курсов
      expect(wrapper.find('[class="btn btn-primary btn-block mb-4"]').exists()).toBe(false) // Нет кнопки сохранения  
      expect(() => {wrapper.find('[class="btn btn-primary btn-block mb-4"]').trigger('click')}).toThrowError() // Не найдет кнопку чтобы нажать
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
      await vm.checkSession()
      await vm.$nextTick()
    })

    it('Отобразится форма регистрации', async()=> {
      expect(wrapper.find('[id="botMessage"]').exists()).toBe(false) // Есть сообщение о проерке капчи
      expect(wrapper.find('[id="loggedMessage"]').exists()).toBe(false) // Нет сообщения об авторизации
      expect(wrapper.find('[class="EntryForm"]').exists()).toBe(true) // Нет курсов
    })

    it('Нажмет кнопку и отправит информацию', async()=> {
      when(axios.post).calledWith('/registeruser/',{
        username: '',
        password1: '',
        password2: ''
      }).thenResolve({})

      expect(wrapper.find('[class="EntryForm"]').exists()).toBe(true) // Есть курсы
      expect(wrapper.find('[class="btn btn-primary btn-block mb-4"]').exists()).toBe(true) // Есть кнопка сохранения

      const buySpy = vi.spyOn(vm, 'setLogin')
      expect(buySpy).not.toHaveBeenCalled()
      wrapper.find('[class="btn btn-primary btn-block mb-4"]').trigger('click')
      expect(buySpy).toHaveBeenCalled()
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
      await vm.checkSession()
      await vm.$nextTick()
    })

    it('Сообщение что уже авторизован', async()=> {
      expect(wrapper.find('[id="botMessage"]').exists()).toBe(false) // Есть сообщение о проерке капчи
      expect(wrapper.find('[id="loggedMessage"]').exists()).toBe(true) // Нет сообщения об авторизации
      expect(wrapper.find('[class="EntryForm"]').exists()).toBe(false) // Есть курсы
    })

    it('Не найдет кнопку входа и не сможет нажать', async()=> {
      expect(wrapper.find('[class="EntryForm"]').exists()).toBe(false) // Нет курсов
      expect(wrapper.find('[class="btn btn-primary btn-block mb-4"]').exists()).toBe(false) // Нет кнопки сохранения  
      expect(() => {wrapper.find('[class="btn btn-primary btn-block mb-4"]').trigger('click')}).toThrowError() // Не найдет кнопку чтобы нажать
    })
  })  
})
