<script lang="ts">
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import { login, user } from '$lib/stores/auth';

	let email = $state('');
	let password = $state('');
	let loading = $state(false);
	let error = $state('');
	let showPassword = $state(false);

	async function handleSubmit(event: Event) {
		event.preventDefault();
		loading = true;
		error = '';

		const result = await login(email, password);

		if (result.success) {
			const currentUser = get(user);
			if (currentUser?.role === 'admin') {
				goto('/dashboard');
			} else if (currentUser?.role === 'service_provider') {
				goto('/dashboard');
			} else {
				goto('/dashboard');
			}
		} else {
			error = result.error || 'Invalid email or password';
		}

		loading = false;
	}
</script>

<svelte:head>
	<title>Login - VBAMS</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-100 p-4">
	<div class="w-full max-w-5xl overflow-hidden rounded-3xl bg-white shadow-2xl">
		<div class="grid md:grid-cols-2">
			<!-- Left Panel - Branding -->
			<div
				class="relative flex flex-col justify-center overflow-hidden bg-gradient-to-br from-blue-600 to-purple-600 p-12 text-white"
			>
				<!-- Decorative circles -->
				<div class="absolute left-10 top-10 h-32 w-32 rounded-full bg-white/10"></div>
				<div class="absolute bottom-10 right-10 h-40 w-40 rounded-full bg-white/10"></div>
				<div class="absolute right-20 top-1/2 h-20 w-20 rounded-full bg-blue-400/20"></div>

				<div class="relative z-10">
					<!-- Logo -->
					<div class="mb-8 flex items-center">
						<div class="mr-3 flex h-12 w-12 items-center justify-center rounded-xl bg-white/20">
							<i class="fas fa-car-crash text-2xl"></i>
						</div>
						<span class="text-2xl font-bold">VBAMS</span>
					</div>

					<!-- Title -->
					<h1 class="mb-6 text-4xl font-bold">Roadside Assistance Platform</h1>

					<!-- Features List -->
					<ul class="space-y-4">
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Get Help Fast</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Real-time GPS Tracking</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Verified Service Providers</span>
						</li>
						<li class="flex items-center">
							<i class="fas fa-check-circle mr-3 text-blue-300"></i>
							<span class="text-blue-50">Transparent Pricing</span>
						</li>
					</ul>

					<!-- Notice -->
					<div class="mt-8 rounded-xl bg-white/10 p-4 backdrop-blur-sm">
						<p class="flex items-center text-sm text-blue-100">
							<i class="fas fa-shield-alt mr-2"></i>
							Join thousands of drivers and providers on the most reliable network.
						</p>
					</div>
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
					<h2 class="mb-2 text-3xl font-bold text-gray-900">Welcome Back</h2>
					<p class="text-gray-500">Sign in to access your dashboard</p>
				</div>

				{#if error}
					<div class="mb-6 rounded-xl border-2 border-red-200 bg-red-50 px-4 py-3 text-red-700">
						<i class="fas fa-exclamation-circle mr-2"></i>
						{error}
					</div>
				{/if}

				<!-- Login Form -->
				<form onsubmit={handleSubmit} class="space-y-5">
					<!-- Email -->
					<div>
						<label for="email" class="mb-2 block text-sm font-medium text-gray-700"
							>Email Address</label
						>
						<input
							id="email"
							type="email"
							bind:value={email}
							placeholder="you@example.com"
							class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
							required
						/>
					</div>

					<!-- Password -->
					<div>
						<label for="password" class="mb-2 block text-sm font-medium text-gray-700"
							>Password</label
						>
						<div class="relative">
							<input
								id="password"
								type={showPassword ? 'text' : 'password'}
								bind:value={password}
								placeholder="••••••••"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 pr-10 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
								required
							/>
							<button
								type="button"
								class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none"
								onclick={() => (showPassword = !showPassword)}
							>
								{#if showPassword}
									<i class="fas fa-eye-slash"></i>
								{:else}
									<i class="fas fa-eye"></i>
								{/if}
							</button>
						</div>
					</div>

					<!-- Forgot Password & Links -->
					<div class="flex items-center justify-between">
						<label
							class="flex cursor-pointer items-center text-sm text-gray-600 hover:text-gray-900"
						>
							<input
								type="checkbox"
								class="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
							/>
							Remember me
						</label>
						<a href="/forgot-password" class="text-sm text-blue-600 hover:text-blue-700">
							Forgot Password?
						</a>
					</div>

					<!-- Submit Button -->
					<button
						type="submit"
						disabled={loading}
						class="w-full rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 py-3 font-semibold text-white transition-all hover:from-blue-700 hover:to-purple-700 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if loading}
							<i class="fas fa-spinner fa-spin mr-2"></i>
							Signing In...
						{:else}
							<i class="fas fa-sign-in-alt mr-2"></i>
							Sign In
						{/if}
					</button>

					<!-- Footer Links -->
					<div class="mt-6 text-center text-sm text-gray-500">
						Don't have an account?
						<a href="/register" class="font-semibold text-blue-600 hover:text-blue-700"
							>Register here</a
						>
					</div>
				</form>
			</div>
		</div>
	</div>
</div>
