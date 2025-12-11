<script lang="ts">
	import { goto } from '$app/navigation';
	import api from '$lib/utils/api';

	let firstName = $state('');
	let lastName = $state('');
	let email = $state('');
	let phone = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let isLoading = $state(false);
	let error = $state('');
	let success = $state(false);

	async function handleRegister() {
		error = '';

		// Validation
		if (!firstName || !lastName || !email || !phone || !password || !confirmPassword) {
			error = 'All fields are required';
			return;
		}

		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length < 6) {
			error = 'Password must be at least 6 characters';
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
				role: 'driver'
			});

			if (response.status === 201) {
				success = true;
				setTimeout(() => {
					goto('/login/driver');
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
	<title>Driver Registration - VBAMS</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-100 p-4">
	<div class="w-full max-w-5xl overflow-hidden rounded-3xl bg-white shadow-2xl">
		<div class="grid md:grid-cols-2">
			<!-- Left Panel - Branding -->
			<div
				class="relative flex flex-col justify-center overflow-hidden bg-gradient-to-br from-blue-600 to-blue-800 p-12 text-white"
			>
				<!-- Decorative circles -->
				<div class="absolute left-10 top-10 h-32 w-32 rounded-full bg-white/10"></div>
				<div class="absolute bottom-10 right-10 h-40 w-40 rounded-full bg-white/10"></div>
				<div class="absolute right-20 top-1/2 h-20 w-20 rounded-full bg-blue-400/20"></div>

				<div class="relative z-10">
					<!-- Logo -->
					<div class="mb-8 flex items-center">
						<div class="mr-3 flex h-12 w-12 items-center justify-center rounded-xl bg-white/20">
							<i class="fas fa-car text-2xl"></i>
						</div>
						<span class="text-2xl font-bold">VBAMS</span>
					</div>

					<!-- Title -->
					<h1 class="mb-6 text-4xl font-bold">Join as a Driver</h1>
					<p class="mb-8 text-blue-100">Get assistance whenever you need it, wherever you are</p>

					<!-- Benefits List -->
					<ul class="space-y-4">
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">24/7 Emergency Assistance</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Track Service Provider in Real-Time</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Manage Multiple Vehicles</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Service History & Ratings</span>
						</li>
					</ul>
				</div>
			</div>

			<!-- Right Panel - Registration Form -->
			<div class="flex flex-col justify-center p-12">
				<!-- Back to Home -->
				<a href="/" class="mb-6 inline-flex items-center text-sm text-gray-500 hover:text-gray-700">
					<i class="fas fa-arrow-left mr-2"></i>
					Back to Home
				</a>

				<!-- Header -->
				<div class="mb-6">
					<h2 class="mb-2 text-3xl font-bold text-gray-900">Create Account</h2>
					<p class="text-gray-500">Join thousands of satisfied drivers</p>
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

				<!-- Registration Form -->
				<form
					onsubmit={(e) => {
						e.preventDefault();
						handleRegister();
					}}
					class="space-y-4"
				>
					<!-- Name Fields -->
					<div class="grid grid-cols-2 gap-4">
						<div>
							<label for="firstName" class="mb-2 block text-sm font-medium text-gray-700"
								>First Name</label
							>
							<input
								id="firstName"
								type="text"
								bind:value={firstName}
								placeholder="John"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
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
								placeholder="Doe"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
								required
							/>
						</div>
					</div>

					<!-- Email -->
					<div>
						<label for="email" class="mb-2 block text-sm font-medium text-gray-700"
							>Email Address</label
						>
						<input
							id="email"
							type="email"
							bind:value={email}
							placeholder="john@example.com"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
							required
						/>
					</div>

					<!-- Phone -->
					<div>
						<label for="phone" class="mb-2 block text-sm font-medium text-gray-700"
							>Phone Number</label
						>
						<input
							id="phone"
							type="tel"
							bind:value={phone}
							placeholder="+1 (555) 123-4567"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
							required
						/>
					</div>

					<!-- Password -->
					<div>
						<label for="password" class="mb-2 block text-sm font-medium text-gray-700"
							>Password</label
						>
						<input
							id="password"
							type="password"
							bind:value={password}
							placeholder="••••••••"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
							required
						/>
					</div>

					<!-- Confirm Password -->
					<div>
						<label for="confirmPassword" class="mb-2 block text-sm font-medium text-gray-700"
							>Confirm Password</label
						>
						<input
							id="confirmPassword"
							type="password"
							bind:value={confirmPassword}
							placeholder="••••••••"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
							required
						/>
					</div>

					<!-- Submit Button -->
					<button
						type="submit"
						disabled={isLoading || success}
						class="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if isLoading}
							<i class="fas fa-spinner fa-spin mr-2"></i>
							Creating Account...
						{:else if success}
							<i class="fas fa-check mr-2"></i>
							Account Created!
						{:else}
							Create Driver Account
						{/if}
					</button>
				</form>

				<!-- Login Link -->
				<div class="mt-6 text-center text-sm text-gray-600">
					Already have an account?
					<a href="/login/driver" class="font-medium text-blue-600 hover:text-blue-700">
						Sign in here
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
