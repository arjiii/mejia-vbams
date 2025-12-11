<script lang="ts">
	import { goto } from '$app/navigation';
	import api from '$lib/utils/api';

	let firstName = $state('');
	let lastName = $state('');
	let email = $state('');
	let phone = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let adminCode = $state('');
	let isLoading = $state(false);
	let error = $state('');
	let success = $state(false);

	async function handleRegister() {
		error = '';

		if (
			!firstName ||
			!lastName ||
			!email ||
			!phone ||
			!password ||
			!confirmPassword ||
			!adminCode
		) {
			error = 'All fields are required';
			return;
		}

		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length < 8) {
			error = 'Admin password must be at least 8 characters';
			return;
		}

		// Simple admin code check (in production, this should be server-side)
		if (adminCode !== 'VBAMS-ADMIN-2024') {
			error = 'Invalid admin authorization code';
			return;
		}

		isLoading = true;

		try {
			const response = await api.post('/auth/register', {
				first_name: firstName,
				last_name: lastName,
				email: email,
				phone: phone,
				password: password,
				role: 'admin'
			});

			if (response.status === 201) {
				success = true;
				setTimeout(() => {
					goto('/login/admin');
				}, 2000);
			}
		} catch (e: any) {
			error = e.response?.data?.detail || 'Registration failed. Please try again.';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Admin Registration - VBAMS</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-100 p-4">
	<div class="w-full max-w-5xl overflow-hidden rounded-3xl bg-white shadow-2xl">
		<div class="grid md:grid-cols-2">
			<!-- Left Panel - Branding -->
			<div
				class="relative flex flex-col justify-center overflow-hidden bg-gradient-to-br from-red-600 to-orange-600 p-12 text-white"
			>
				<div class="absolute left-10 top-10 h-32 w-32 rounded-full bg-white/10"></div>
				<div class="absolute bottom-10 right-10 h-40 w-40 rounded-full bg-white/10"></div>
				<div class="absolute right-20 top-1/2 h-20 w-20 rounded-full bg-orange-400/20"></div>

				<div class="relative z-10">
					<div class="mb-8 flex items-center">
						<div class="mr-3 flex h-12 w-12 items-center justify-center rounded-xl bg-white/20">
							<i class="fas fa-shield-alt text-2xl"></i>
						</div>
						<span class="text-2xl font-bold">VBAMS</span>
					</div>

					<h1 class="mb-6 text-4xl font-bold">Admin Registration</h1>
					<p class="mb-8 text-red-100">Secure access for system administrators</p>

					<ul class="space-y-4">
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-red-300"></i>
							<span class="text-red-50">Full System Control</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-red-300"></i>
							<span class="text-red-50">User & Provider Management</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-red-300"></i>
							<span class="text-red-50">Analytics & Reports</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-red-300"></i>
							<span class="text-red-50">System Configuration</span>
						</li>
					</ul>

					<div class="mt-8 rounded-xl bg-white/10 p-4 backdrop-blur-sm">
						<p class="flex items-center text-sm text-red-100">
							<i class="fas fa-exclamation-triangle mr-2"></i>
							Admin access requires authorization code
						</p>
					</div>
				</div>
			</div>

			<!-- Right Panel - Registration Form -->
			<div class="flex flex-col justify-center p-12">
				<a href="/" class="mb-6 inline-flex items-center text-sm text-gray-500 hover:text-gray-700">
					<i class="fas fa-arrow-left mr-2"></i>
					Back to Home
				</a>

				<div class="mb-6">
					<h2 class="mb-2 text-3xl font-bold text-gray-900">Admin Account</h2>
					<p class="text-gray-500">Create administrative credentials</p>
				</div>

				{#if success}
					<div
						class="mb-6 rounded-xl border-2 border-green-200 bg-green-50 px-4 py-3 text-green-700"
					>
						<i class="fas fa-check-circle mr-2"></i>
						Registration successful! Redirecting to login...
					</div>
				{/if}

				{#if error}
					<div class="mb-6 rounded-xl border-2 border-red-200 bg-red-50 px-4 py-3 text-red-700">
						<i class="fas fa-exclamation-circle mr-2"></i>
						{error}
					</div>
				{/if}

				<form
					onsubmit={(e) => {
						e.preventDefault();
						handleRegister();
					}}
					class="space-y-4"
				>
					<div class="grid grid-cols-2 gap-4">
						<div>
							<label for="firstName" class="mb-2 block text-sm font-medium text-gray-700"
								>First Name</label
							>
							<input
								id="firstName"
								type="text"
								bind:value={firstName}
								placeholder="Admin"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
								required
							/>
						</div>
						<div>
							<label for="lastName" class="mb-2 block text-sm font-medium text-gray-700"
								>Last Name</label
							>
							<input
								id="lastName"
								type="text"
								bind:value={lastName}
								placeholder="User"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
								required
							/>
						</div>
					</div>

					<div>
						<label for="email" class="mb-2 block text-sm font-medium text-gray-700"
							>Admin Email</label
						>
						<input
							id="email"
							type="email"
							bind:value={email}
							placeholder="admin@vbams.com"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
							required
						/>
					</div>

					<div>
						<label for="phone" class="mb-2 block text-sm font-medium text-gray-700"
							>Phone Number</label
						>
						<input
							id="phone"
							type="tel"
							bind:value={phone}
							placeholder="+1 (555) 000-0000"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
							required
						/>
					</div>

					<div>
						<label for="adminCode" class="mb-2 block text-sm font-medium text-gray-700">
							<i class="fas fa-key mr-1"></i>
							Admin Authorization Code
						</label>
						<input
							id="adminCode"
							type="text"
							bind:value={adminCode}
							placeholder="Enter admin code"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
							required
						/>
					</div>

					<div>
						<label for="password" class="mb-2 block text-sm font-medium text-gray-700"
							>Password (min. 8 characters)</label
						>
						<input
							id="password"
							type="password"
							bind:value={password}
							placeholder="••••••••"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
							required
						/>
					</div>

					<div>
						<label for="confirmPassword" class="mb-2 block text-sm font-medium text-gray-700"
							>Confirm Password</label
						>
						<input
							id="confirmPassword"
							type="password"
							bind:value={confirmPassword}
							placeholder="••••••••"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-red-500"
							required
						/>
					</div>

					<button
						type="submit"
						disabled={isLoading || success}
						class="w-full rounded-xl bg-gradient-to-r from-red-600 to-orange-600 py-3 font-semibold text-white transition-all hover:from-red-700 hover:to-orange-700 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if isLoading}
							<i class="fas fa-spinner fa-spin mr-2"></i>
							Creating Account...
						{:else if success}
							<i class="fas fa-check mr-2"></i>
							Account Created!
						{:else}
							<i class="fas fa-shield-alt mr-2"></i>
							Create Admin Account
						{/if}
					</button>
				</form>

				<div class="mt-6 text-center text-sm text-gray-600">
					Already have an account?
					<a href="/login/admin" class="font-medium text-red-600 hover:text-red-700">
						Sign in here
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
