import { browser } from '$app/environment';
import { writable, type Writable, get } from 'svelte/store';
import api from '$lib/utils/api';

// Use Vite env var for API base (falls back to localhost:8000/api).
const API_BASE_URL = (import.meta.env?.VITE_API_BASE as string) || '/api';

// Export stores so components can subscribe or use the $ shorthand in .svelte files
export const isAuthenticated: Writable<boolean> = writable(false);
export const user: Writable<any> = writable(null);
export const token: Writable<string | null> = writable(null);

// Keep a local copy of the token for use inside async functions
let currentToken: string | null = null;
token.subscribe((v) => (currentToken = v));

// Initialize auth state from localStorage
if (browser) {
	const storedToken = localStorage.getItem('token');
	if (storedToken) {
		token.set(storedToken);
		isAuthenticated.set(true);
		loadUserData();
	}
}

// Load user data
async function loadUserData() {
	try {
		// use shared axios instance which already attaches Authorization from localStorage
		const response = await api.get('/auth/me');
		// backend returns the user object directly (not wrapped in { user: ... })
		user.set(response.data);
	} catch (error) {
		console.error('Error loading user data:', error);
		logout();
	}
}

// Login function
export async function login(email: string, password: string) {
	try {
		const response = await api.post('/auth/login', {
			email,
			password
		});

		const { access_token } = response.data;

		if (browser) {
			localStorage.setItem('token', access_token);
		}

		token.set(access_token);

		// fetch the current user from the backend (login response doesn't include user)
		await loadUserData();
		isAuthenticated.set(true);

		return { success: true };
	} catch (error: any) {
		return {
			success: false,
			error: error.response?.data?.detail || 'Login failed'
		};
	}
}



// Register function
export async function register(userData: any) {
	try {
		const response = await api.post('/auth/register', userData);

		// Some backends return the token on register, others return only the user object.
		const accessToken = response.data?.access_token || response.data?.accessToken || response.data?.token;

		if (accessToken) {
			if (browser) {
				localStorage.setItem('token', accessToken);
			}

			token.set(accessToken);
			user.set(response.data?.user || response.data);
			isAuthenticated.set(true);
			return { success: true };
		}

		// If no token returned, attempt to auto-login with the credentials provided
		// (this keeps UX smooth for APIs that don't return a token at register)
		if (userData.email && userData.password) {
			const loginResult = await login(userData.email, userData.password);
			if (loginResult.success) {
				return { success: true };
			}
			// Auto-login failed — fallthrough to return success but ask user to login
			return {
				success: false,
				error: 'Registered successfully but automatic login failed. Please sign in.'
			};
		}

		// If we reach here, registration succeeded but we couldn't determine token or auto-login
		return { success: true };
	} catch (error: any) {
		// Try to extract useful error messages from common shapes
		const serverMsg =
			error?.response?.data?.detail ||
			error?.response?.data?.message ||
			error?.response?.data ||
			error?.message ||
			'Registration failed';
		return {
			success: false,
			error: typeof serverMsg === 'string' ? serverMsg : JSON.stringify(serverMsg)
		};
	}
}

// Logout function
export function logout() {
	if (browser) {
		localStorage.removeItem('token');
	}
	token.set(null);
	user.set(null);
	isAuthenticated.set(false);
}

// Update user location
export async function updateLocation(latitude: number, longitude: number) {
	try {
		await api.put('/auth/update-location', { latitude, longitude });

		// update local user object if present
		const u = get(user);
		if (u) {
			u.latitude = latitude;
			u.longitude = longitude;
			user.set(u);
		}

		return { success: true };
	} catch (error: any) {
		return {
			success: false,
			error: error.response?.data?.detail || 'Location update failed'
		};
	}
}
