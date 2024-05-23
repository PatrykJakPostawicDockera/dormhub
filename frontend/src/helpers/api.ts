import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/stores/auth';

const url = import.meta.env.VITE_API_URL;

async function api<T>(
  endpoint: string,
  method: string,
  useToken: boolean,
  bodyContent?: any,
): Promise<T | null> {
  const toast = useToast();
  const authStore = useAuthStore();
  const headers: any = {};
  let requestBody: any = {};

  const setUrl = () => {
    if (endpoint.includes('?')) return `${url}/${endpoint}`;
    return `${url}/${endpoint}/`;
  };

  const setContentTypeAndBody = () => {
    if (method === 'POST' || method === 'PUT') {
      headers['Content-Type'] = 'application/json';
      requestBody = JSON.stringify(bodyContent);
      return;
    }
  };

  const setAuthHeader = () => {
    if (useToken) {
      const token = authStore.getToken;
      if (token) headers['Authorization'] = `Bearer ${token}`;
    }
  };

  const handleResponse = async (res: Response): Promise<any> => {
    if (res.ok) {
      if (res.headers.get('Content-Type')?.includes('application/json')) {
        return res.json();
      }
      if (res.headers.get('Content-Type')?.includes('image')) return res.blob();
      return res.text();
    }
    if (res.status === 401 && endpoint !== 'users/login') {
      toast.error('Your session has expired. Please log in again.');
      await authStore.logout();
      return Promise.reject('Unauthorized');
    }
    toast.error(res.statusText);
    return Promise.reject('Error');
  };

  try {
    setContentTypeAndBody();
    setAuthHeader();

    const response = await fetch(setUrl(), {
      method,
      headers,
      body: (method === 'POST' || method === 'PUT') && requestBody ? requestBody : undefined,
    });
    return await handleResponse(response);
  } catch (err) {
    return null;
  }
}

// Helper class for API calls
class apiHelper {
  static async get<T>(endpoint: string, useToken: boolean = false): Promise<T | null> {
    return await api<T>(endpoint, 'GET', useToken);
  }

  static async post<T>(
    endpoint: string,
    bodyContent: any,
    useToken: boolean = false,
  ): Promise<T | null> {
    return await api<T>(endpoint, 'POST', useToken, bodyContent);
  }

  static async postFormData<T>(
    endpoint: string,
    bodyContent: any,
    useToken: boolean = false,
  ): Promise<T | null> {
    return await api<T>(endpoint, 'POST', useToken, bodyContent);
  }

  static async put<T>(
    endpoint: string,
    bodyContent: any,
    useToken: boolean = false,
  ): Promise<T | null> {
    return await api<T>(endpoint, 'PUT', useToken, bodyContent);
  }

  static async delete<T>(endpoint: string, useToken: boolean = false): Promise<T | null> {
    return await api<T>(endpoint, 'DELETE', useToken);
  }
}

// Shared API instance
export const apiInstance = apiHelper;
