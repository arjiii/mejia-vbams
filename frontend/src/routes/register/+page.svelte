<script lang="ts">
	import { goto } from '$app/navigation';
	import { register } from '$lib/stores/auth';
	import { page } from '$app/stores';
	import { API_BASE_URL } from '$lib/utils/api';

	let firstName = '';
	let lastName = '';
	let email = '';
	let phone = '';
	let password = '';
	let role = 'driver';
	let loading = false;
	let error = '';

	// Set role from URL params
	$: if ($page.url.searchParams.get('role') === 'service_provider') {
		role = 'service_provider';
	}

	async function handleSubmit() {
		if (!firstName || !lastName || !email || !phone || !password) {
			error = 'Please fill in all fields';
			return;
		}

		loading = true;
		error = '';

		const userData = {
			first_name: firstName,
			last_name: lastName,
			email,
			phone,
			password,
			role
		};

		const result = await register(userData);

		if (result.success) {
			goto('/dashboard');
		} else {
			// Provide clearer guidance for common connectivity errors
			if (
				typeof result.error === 'string' &&
				(result.error.includes('Not Found') || result.error.includes('404'))
			) {
				error = `Backend endpoint not found. Frontend used ${API_BASE_URL}. Make sure the backend is running and that VITE_API_BASE points to the correct host/port (for example http://localhost:8001/api).`;
			} else if (
				typeof result.error === 'string' &&
				(result.error.includes('Network Error') || result.error.includes('ECONNREFUSED'))
			) {
				error =
					'Network error connecting to backend. Check that the backend server is running and reachable from this machine.';
			} else {
				error = result.error;
			}
		}

		loading = false;
	}
</script>

<svelte:head>
	<title>Register - VBAMS</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
	<div class="w-full max-w-md space-y-8">
		<div class="text-center">
			<div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
				<i class="fas fa-car-crash text-3xl text-blue-600"></i>
			</div>
			<h2 class="mt-6 text-3xl font-extrabold text-gray-900">Create your account</h2>
			<p class="mt-2 text-sm text-gray-600">
				Or
				<a href="/login" class="font-medium text-blue-600 hover:text-blue-500">
					sign in to your existing account
				</a>
			</p>
		</div>

		<div class="rounded-xl border border-gray-100 bg-white px-4 py-8 shadow-xl sm:px-10">
			<form class="space-y-6" on:submit|preventDefault={handleSubmit}>
				{#if error}
					<div
						class="flex items-center rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-600"
					>
						<i class="fas fa-exclamation-circle mr-2"></i>
						{error}
					</div>
				{/if}

				<div class="space-y-4">
					<div class="grid grid-cols-2 gap-4">
						<div>
							<label for="firstName" class="block text-sm font-medium text-gray-700"
								>First Name</label
							>
							<input
								id="firstName"
								name="firstName"
								type="text"
								required
								bind:value={firstName}
								class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
								placeholder="First name"
							/>
						</div>
						<div>
							<label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label
							>
							<input
								id="lastName"
								name="lastName"
								type="text"
								required
								bind:value={lastName}
								class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
								placeholder="Last name"
							/>
						</div>
					</div>

					<div>
						<label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
						<input
							id="email"
							name="email"
							type="email"
							autocomplete="email"
							required
							bind:value={email}
							class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
							placeholder="you@example.com"
						/>
					</div>

					<div>
						<label for="phone" class="block text-sm font-medium text-gray-700">Phone Number</label>
						<input
							id="phone"
							name="phone"
							type="tel"
							autocomplete="tel"
							required
							bind:value={phone}
							class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
							placeholder="+1 (555) 123-4567"
						/>
					</div>

					<div>
						<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
						<input
							id="password"
							name="password"
							type="password"
							autocomplete="new-password"
							required
							bind:value={password}
							class="mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
							placeholder="••••••••"
						/>
					</div>

					<div>
						<label for="role" class="block text-sm font-medium text-gray-700">I am a...</label>
						<select
							id="role"
							name="role"
							bind:value={role}
							class="mt-1 block w-full rounded-lg border-gray-300 py-2 pl-3 pr-10 text-base focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
						>
							<option value="driver">Driver (I need assistance)</option>
							<option value="service_provider">Service Provider (I offer assistance)</option>
						</select>
					</div>
				</div>

				<div>
					<button
						type="submit"
						disabled={loading}
						class="flex w-full justify-center rounded-lg border border-transparent bg-blue-600 px-4 py-3 text-sm font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
					>
						{#if loading}
							<i class="fas fa-spinner fa-spin mr-2"></i>
						{/if}
						Create Account
					</button>
				</div>
			</form>
		</div>
	</div>
</div>
