<script lang="ts">
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/auth';

	let email = $state('driver@test.com');
	let password = $state('password123');
	let isLoading = $state(false);
	let error = $state('');

	async function handleLogin() {
		error = '';
		isLoading = true;

		try {
			const result = await login(email, password);

			if (result.success) {
				goto('/dashboard');
			} else {
				error = result.error || 'Login failed. Please check your credentials.';
			}
		} catch (e) {
			error = 'Network error. Please make sure the backend server is running.';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Driver Login - VBAMS</title>
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
					<h1 class="mb-6 text-4xl font-bold">Driver Portal</h1>

					<!-- Features List -->
					<ul class="space-y-4">
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Emergency Assistance</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Vehicle Management</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Real-time Tracking</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">24/7 Support</span>
						</li>
					</ul>
				</div>
			</div>

			<!-- Right Panel - Login Form -->
			<div class="flex flex-col justify-center p-12">
				<!-- Back to Home -->
				<a href="/" class="mb-6 inline-flex items-center text-sm text-gray-500 hover:text-gray-700">
					<i class="fas fa-arrow-left mr-2"></i>
					Back to Home
				</a>

				<!-- Header -->
				<div class="mb-8">
					<h2 class="mb-2 text-3xl font-bold text-gray-900">Login</h2>
					<p class="text-gray-500">Welcome back! Please login to your account.</p>
				</div>

				{#if error}
					<div class="mb-6 rounded-xl border-2 border-red-200 bg-red-50 px-4 py-3 text-red-700">
						<i class="fas fa-exclamation-circle mr-2"></i>
						{error}
					</div>
				{/if}

				<!-- Login Form -->
				<form
					onsubmit={(e) => {
						e.preventDefault();
						handleLogin();
					}}
					class="space-y-5"
				>
					<!-- Email -->
					<div>
						<label for="email" class="mb-2 block text-sm font-medium text-gray-700"
							>Email or Phone Number</label
						>
						<input
							id="email"
							type="text"
							bind:value={email}
							placeholder="your@email.com or mobile number"
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

					<!-- Forgot Password -->
					<div class="text-right">
						<a href="/forgot-password" class="text-sm text-blue-600 hover:text-blue-700">
							Forgot Password?
						</a>
					</div>

					<!-- Submit Button -->
					<button
						type="submit"
						disabled={isLoading}
						class="w-full rounded-xl bg-blue-600 py-3 font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if isLoading}
							<i class="fas fa-spinner fa-spin mr-2"></i>
							Signing in...
						{:else}
							Sign In
						{/if}
					</button>
				</form>

				<!-- Register Link -->
				<div class="mt-6 text-center text-sm text-gray-600">
					Don't have an account?
					<a href="/register/driver" class="font-medium text-blue-600 hover:text-blue-700">
						Register here
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
