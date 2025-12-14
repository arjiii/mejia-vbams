import axios from 'axios';
import { browser } from '$app/environment';

// Determine the API base URL based on environment
// Production: Railway backend
// Development: localhost
const isDev = import.meta.env.DEV;
const defaultBaseURL = isDev
	? 'http://localhost:9000'
	: 'https://mejia-vbams-production.up.railway.app';

export let API_BASE_URL = import.meta.env?.VITE_API_BASE || defaultBaseURL;

// Create axios instance with initial base
const api = axios.create({ baseURL: API_BASE_URL, timeout: 10000 });

if (browser) {
	console.info('[VBAMS] API base URL set to', API_BASE_URL);
	console.info('[VBAMS] Environment:', isDev ? 'development' : 'production');
}

// Add request interceptor to include auth token
api.interceptors.request.use(
	(config) => {
		if (browser) {
			const token = localStorage.getItem('token');
			if (token) {
				config.headers.Authorization = `Bearer ${token}`;
			}
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

// Add response interceptor for error handling
api.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401) {
			// Token expired or invalid
			if (browser) {
				localStorage.removeItem('token');
				window.location.href = '/login';
			}
		}
		return Promise.reject(error);
	}
);

// API functions
export const vehicleAPI = {
	getAll: () => api.get('/vehicles'),
	getById: (id: number) => api.get(`/vehicles/${id}`),
	create: (data: any) => api.post('/vehicles', data),
	update: (id: number, data: any) => api.put(`/vehicles/${id}`, data),
	delete: (id: number) => api.delete(`/vehicles/${id}`),
	updateMileage: (id: number, mileage: number) => api.put(`/vehicles/${id}/mileage`, { mileage })
};

export const breakdownAPI = {
	getAll: () => api.get('/breakdowns'),
	getById: (id: number) => api.get(`/breakdowns/${id}`),
	create: (data: any) => api.post('/breakdowns', data),
	update: (id: number, data: any) => api.put(`/breakdowns/${id}`, data),
	updateStatus: (id: number, status: string) => api.put(`/breakdowns/${id}/status`, { status }),
	getNearby: (lat: number, lng: number, radius: number = 10) =>
		api.get(`/breakdowns/nearby/${lat}/${lng}?radius=${radius}`)
};

export const assistanceAPI = {
	getAll: () => api.get('/assistance'),
	getById: (id: number) => api.get(`/assistance/${id}`),
	create: (data: any) => api.post('/assistance', data),
	update: (id: number, data: any) => api.put(`/assistance/${id}`, data),
	accept: (id: number) => api.put(`/assistance/${id}/accept`),
	reject: (id: number) => api.put(`/assistance/${id}/reject`),
	complete: (id: number, data: any) => api.put(`/assistance/${id}/complete`, data)
};

export const serviceProviderAPI = {
	register: (data: any) => api.post('/service-providers/register', data),
	getProfile: () => api.get('/service-providers/profile'),
	updateProfile: (data: any) => api.put('/service-providers/profile', data),
	updateLocation: (lat: number, lng: number) => api.put('/service-providers/location', { latitude: lat, longitude: lng }),
	updateOnlineStatus: (isOnline: boolean) => api.put('/service-providers/online-status', { is_online: isOnline }),
	getNearby: (lat: number, lng: number, radius: number = 50, serviceType?: string) =>
		api.get(`/service-providers/nearby/${lat}/${lng}?radius=${radius}&service_type=${serviceType || ''}`)
};

export const userAPI = {
	getProfile: () => api.get('/auth/me'),
	updateProfile: (data: any) => api.put('/users/profile', data),
	updateLocation: (lat: number, lng: number) => api.put('/auth/update-location', { latitude: lat, longitude: lng })
};

export default api;
