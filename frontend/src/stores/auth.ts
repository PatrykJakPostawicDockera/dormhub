import { defineStore } from 'pinia';
import router from '@/router';
import type { UserRegisterModel } from '@/models/user.model';
import { apiInstance } from '@/helpers/api';
import { useToast } from 'vue-toastification';
import type { JwtPayload } from '@/helpers/jwt';
import decode from '@/helpers/jwt';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuth: false,
    token: '',
    tokenData: {} as JwtPayload,
  }),
  getters: {
    isAuthenticated: (state) => {
      return state.isAuth;
    },
    getToken: (state) => {
      return state.token;
    },
    getTokenData: (state) => {
      return state.tokenData;
    },
  },
  actions: {
    async login(username: string, password: string) {
      const response = await apiInstance.post<string>('users/login', {
        Email: username,
        Password: password,
      });
      if (response) {
        this.isAuth = true;
        this.token = response;
        this.tokenData = decode(response);
        await router.push('/app');
      } else {
        const toast = useToast();
        toast.error('Invalid credentials');
      }
    },
    async logout() {
      this.isAuth = false;
      this.token = '';
      this.tokenData = {} as JwtPayload;
      await router.push('/');
    },
    async register(data: UserRegisterModel) {
      const response = await apiInstance.post<string>('users/register', data);
      if (response) {
        this.isAuth = true;
        this.token = response;
        this.tokenData = decode(response);
        await router.push('/app');
      }
    },
  },
  persist: true,
});
