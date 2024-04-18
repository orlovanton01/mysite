import { shallowMount, mount, flushPromises, enableAutoUnmount } from '@vue/test-utils'
import {YOUR_V2_SITEKEY_HERE, YOUR_V3_SITEKEY_HERE} from '@/config'
import { createHead } from '@unhead/vue'
import { VueRecaptchaPlugin } from 'vue-recaptcha/head'
import { beforeEach, describe, vi  } from 'vitest'
import axios from 'axios'
import { when } from 'vitest-when'
import App from '@/App.vue'

vi.mock('axios')

describe('AppView.vue', () => {  
  let wrapper
  let vm
  beforeEach(async ()=>{
    wrapper = shallowMount(App, {
    // wrapper = mount(App, {
      global: {
        stubs: {
          'RouterView': { template: '<div/>' },
          'router-view': { template: '<div/>' },
        },
      }
    })
    await flushPromises()
    vm = wrapper.vm
  })

  enableAutoUnmount(afterEach)

  describe('Гость',()=>{
    beforeEach(async()=>{
      when(axios.get).calledWith('/session/').thenResolve({
        data: {
          'isAuthenticated':false
        }
      })
      // await vm.Req()
      await vm.$nextTick()
    })

    it('Имя содержит Гость',async()=>{
      expect(wrapper.find('[id="username"]').text()).toContain('Гость')
    })

    it('Отобразятся кнопки входа и регистрации', async()=> {
      expect(wrapper.find('[id="login"]').exists()).toBe(true) // Есть кнопка входа
      expect(wrapper.find('[id="register"]').exists()).toBe(true) // Есть кнопка регистрации
      expect(wrapper.find('[id="logout"]').exists()).toBe(false) // Нет кнопки выхода
    })

    it('Сможет нажать вход', async()=> {
      expect(()=>{wrapper.find('[id="login"]').trigger('click')}).not.toThrowError()
    })

    it('Сможет нажать регистрацию', async()=> {
      expect(()=>{wrapper.find('[id="register"]').trigger('click')}).not.toThrowError()
    })

    
    it('Не сможет нажать выход', async()=> {
      when(axios.post).calledWith('/logout/').thenResolve({})

      expect(wrapper.find('[id="logout"]').exists()).toBe(false)

      const buySpy = vi.spyOn(vm, 'Logout')
      expect(buySpy).not.toHaveBeenCalled()
      expect(()=>{wrapper.find('[id="logout"]').trigger('click')}).toThrowError()
      expect(buySpy).not.toHaveBeenCalled()
    })
    
  })
  
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  describe('Пользователь',()=>{
    beforeEach(async()=>{
      when(axios.get).calledWith('/session/').thenResolve({
        data: {
          'isAuthenticated':true,
          'username': "TestUser",
          'id': 1
        }
      })
      await vm.Req()
      await vm.$nextTick()
    })

    it('Имя содержит имя TestUser', async()=> {
      expect(wrapper.find('[id="username"]').text()).toContain('TestUser')
    })

    it('Есть только кнопка выхода', async()=> {
      expect(wrapper.find('[id="login"]').exists()).toBe(false) // Нет кнопки входа
      expect(wrapper.find('[id="register"]').exists()).toBe(false) // Нет кнопки регистрации
      expect(wrapper.find('[id="logout"]').exists()).toBe(true) // Есть кнопка выхода
    })

    it('Не сможет нажать вход', async()=> {
      expect(()=>{wrapper.find('[id="login"]').trigger('click')}).toThrowError()
    })

    it('Не сможет нажать регистрацию', async()=> {
      expect(()=>{wrapper.find('[id="register"]').trigger('click')}).toThrowError()
    })
    
    it('Сможет нажать выход', async()=> {
      when(axios.post).calledWith('/logout/').thenResolve({})

      expect(wrapper.find('[id="logout"]').exists()).toBe(true)

      const buySpy = vi.spyOn(vm, 'Logout')
      expect(buySpy).not.toHaveBeenCalled()
      expect(()=>{wrapper.find('[id="logout"]').trigger('click')}).not.toThrowError()
      expect(buySpy).toHaveBeenCalled()
    })
  })  
})
