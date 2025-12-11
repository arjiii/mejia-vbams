<script lang="ts">
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/auth';

	let email = $state('provider@test.com');
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
	<title>Service Provider Login - VBAMS</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-100 p-4">
	<div class="w-full max-w-5xl overflow-hidden rounded-3xl bg-white shadow-2xl">
		<div class="grid md:grid-cols-2">
			<!-- Left Panel - Branding -->
			<div
				class="relative flex flex-col justify-center overflow-hidden bg-gradient-to-br from-purple-600 to-purple-800 p-12 text-white"
			>
				<!-- Decorative circles -->
				<div class="absolute left-10 top-10 h-32 w-32 rounded-full bg-white/10"></div>
				<div class="absolute bottom-10 right-10 h-40 w-40 rounded-full bg-white/10"></div>
				<div class="absolute right-20 top-1/2 h-20 w-20 rounded-full bg-purple-400/20"></div>

				<div class="relative z-10">
					<!-- Logo -->
					<div class="mb-8 flex items-center">
						<div class="mr-3 flex h-12 w-12 items-center justify-center rounded-xl bg-white/20">
							<i class="fas fa-tools text-2xl"></i>
						</div>
						<span class="text-2xl font-bold">VBAMS</span>
					</div>

					<!-- Title -->
					<h1 class="mb-6 text-4xl font-bold">Service Provider Portal</h1>

					<!-- Features List -->
					<ul class="space-y-4">
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-purple-300"></i>
							<span class="text-purple-50">Job Requests</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-purple-300"></i>
							<span class="text-purple-50">Earnings Tracking</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-purple-300"></i>
							<span class="text-purple-50">Schedule Management</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-purple-300"></i>
							<span class="text-purple-50">Rating & Reviews</span>
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
					<p class="text-gray-500">Access your service provider dashboard.</p>
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
							>Business Email</label
						>
						<input
							id="email"
							type="email"
							bind:value={email}
							placeholder="business@email.com"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-purple-500"
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
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-purple-500"
							required
						/>
					</div>

					<!-- Forgot Password -->
					<div class="text-right">
						<a href="/forgot-password" class="text-sm text-purple-600 hover:text-purple-700">
							Forgot Password?
						</a>
					</div>

					<!-- Submit Button -->
					<button
						type="submit"
						disabled={isLoading}
						class="w-full rounded-xl bg-purple-600 py-3 font-semibold text-white transition-colors hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-50"
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
					<a href="/register/provider" class="font-medium text-purple-600 hover:text-purple-700">
						Register your business
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
