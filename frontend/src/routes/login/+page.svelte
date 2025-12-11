<script lang="ts">
	import { goto } from '$app/navigation';
	import { login, user, isAuthenticated, token } from '$lib/stores/auth';

	let email = '';
	let password = '';
	let loading = false;
	let error = '';
	let showQuickLogin = true; // Set to false in production

	async function handleSubmit(event: Event) {
		event.preventDefault();
		loading = true;
		error = '';

		const result = await login(email, password);

		if (result.success) {
			goto('/dashboard');
		} else {
			error = result.error || 'Invalid email or password';
		}

		loading = false;
	}

	function quickLogin(role: string, testEmail: string) {
		// Set mock token
		token.set('mock-dev-token-' + role);

		// Set user
		user.set({
			id: Math.random().toString(),
			email: testEmail,
			first_name:
				role === 'service_provider' ? 'Service' : role.charAt(0).toUpperCase() + role.slice(1),
			last_name: 'Test',
			phone: '+1234567890',
			role: role,
			created_at: new Date().toISOString()
		});

		// Set authenticated
		isAuthenticated.set(true);

		// Navigate to dashboard
		goto('/dashboard');
	}
</script>

<svelte:head>
	<title>Login - VBAMS</title>
</svelte:head>

<div
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 px-4 py-12 sm:px-6 lg:px-8"
>
	<div class="w-full max-w-2xl">
		<!-- Quick Test Login Section -->
		{#if showQuickLogin}
			<div
				class="mb-6 rounded-2xl border-2 border-dashed border-blue-300 bg-gradient-to-r from-blue-50 to-purple-50 p-6 shadow-xl"
			>
				<div class="mb-4 flex items-center justify-between">
					<div class="flex items-center">
						<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
							<i class="fas fa-flask text-white"></i>
						</div>
						<div class="ml-3">
							<h3 class="text-lg font-bold text-gray-900">Quick Test Access</h3>
							<p class="text-xs text-gray-600">For developers - One-click login for each role</p>
						</div>
					</div>
					<button
						onclick={() => (showQuickLogin = false)}
						class="rounded-lg p-2 text-gray-600 transition-colors hover:bg-white"
						aria-label="Close quick login panel"
					>
						<i class="fas fa-times"></i>
					</button>
				</div>

				<div class="grid grid-cols-1 gap-3 md:grid-cols-3">
					<!-- Driver Card -->
					<div class="group">
						<button
							onclick={() => quickLogin('driver', 'driver@test.com')}
							class="flex w-full flex-col items-center rounded-xl border-2 border-blue-200 bg-white p-4 text-center transition-all hover:border-blue-400 hover:bg-blue-50 hover:shadow-lg"
						>
							<div
								class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-blue-100 transition-colors group-hover:bg-blue-200"
							>
								<i class="fas fa-car text-2xl text-blue-600"></i>
							</div>
							<span class="mb-1 font-bold text-gray-900">Driver Dashboard</span>
							<span class="text-xs text-gray-500">driver@test.com</span>
							<div class="mt-3 flex items-center text-xs font-medium text-blue-600">
								<i class="fas fa-bolt mr-1"></i>
								Quick Login
							</div>
						</button>
						<a
							href="/login/driver"
							class="mt-2 block text-center text-xs font-medium text-blue-600 hover:text-blue-800"
						>
							<i class="fas fa-external-link-alt mr-1"></i>
							Role-specific page
						</a>
					</div>

					<!-- Service Provider Card -->
					<div class="group">
						<button
							onclick={() => quickLogin('service_provider', 'provider@test.com')}
							class="flex w-full flex-col items-center rounded-xl border-2 border-purple-200 bg-white p-4 text-center transition-all hover:border-purple-400 hover:bg-purple-50 hover:shadow-lg"
						>
							<div
								class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-purple-100 transition-colors group-hover:bg-purple-200"
							>
								<i class="fas fa-tools text-2xl text-purple-600"></i>
							</div>
							<span class="mb-1 font-bold text-gray-900">Service Provider</span>
							<span class="text-xs text-gray-500">provider@test.com</span>
							<div class="mt-3 flex items-center text-xs font-medium text-purple-600">
								<i class="fas fa-bolt mr-1"></i>
								Quick Login
							</div>
						</button>
						<a
							href="/login/provider"
							class="mt-2 block text-center text-xs font-medium text-purple-600 hover:text-purple-800"
						>
							<i class="fas fa-external-link-alt mr-1"></i>
							Role-specific page
						</a>
					</div>

					<!-- Admin Card -->
					<div class="group">
						<button
							onclick={() => quickLogin('admin', 'admin@test.com')}
							class="flex w-full flex-col items-center rounded-xl border-2 border-red-200 bg-white p-4 text-center transition-all hover:border-red-400 hover:bg-red-50 hover:shadow-lg"
						>
							<div
								class="mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-red-100 transition-colors group-hover:bg-red-200"
							>
								<i class="fas fa-shield-alt text-2xl text-red-600"></i>
							</div>
							<span class="mb-1 font-bold text-gray-900">Admin Panel</span>
							<span class="text-xs text-gray-500">admin@test.com</span>
							<div class="mt-3 flex items-center text-xs font-medium text-red-600">
								<i class="fas fa-bolt mr-1"></i>
								Quick Login
							</div>
						</button>
						<a
							href="/login/admin"
							class="mt-2 block text-center text-xs font-medium text-red-600 hover:text-red-800"
						>
							<i class="fas fa-external-link-alt mr-1"></i>
							Role-specific page
						</a>
					</div>
				</div>

				<div class="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-3">
					<div class="flex items-center">
						<i class="fas fa-info-circle mr-2 text-amber-600"></i>
						<p class="text-xs text-amber-800">
							<strong>Dev Mode:</strong> Click any role to instantly access that dashboard.
							Password: <code class="rounded bg-amber-100 px-1">password</code>
						</p>
					</div>
				</div>
			</div>
		{/if}

		<!-- Main Login Card -->
		<div class="space-y-8">
			<div class="text-center">
				<div
					class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-purple-600 shadow-lg"
				>
					<i class="fas fa-car-crash text-3xl text-white"></i>
				</div>
				<h2 class="mt-6 text-3xl font-extrabold text-gray-900">Welcome back</h2>
				<p class="mt-2 text-sm text-gray-600">Sign in to access your dashboard</p>
			</div>

			<div class="rounded-2xl border border-gray-100 bg-white px-6 py-8 shadow-xl sm:px-10">
				<form class="space-y-6" onsubmit={handleSubmit}>
					{#if error}
						<div
							class="flex items-center rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-600"
						>
							<i class="fas fa-exclamation-circle mr-2"></i>
							{error}
						</div>
					{/if}

					<div>
						<label for="email" class="mb-1 block text-sm font-medium text-gray-700"
							>Email address</label
						>
						<div class="relative rounded-md shadow-sm">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<i class="fas fa-envelope text-gray-400"></i>
							</div>
							<input
								id="email"
								name="email"
								type="email"
								autocomplete="email"
								required
								bind:value={email}
								class="block w-full rounded-lg border border-gray-300 py-3 pl-10 pr-3 transition-all focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
								placeholder="you@example.com"
							/>
						</div>
					</div>

					<div>
						<label for="password" class="mb-1 block text-sm font-medium text-gray-700"
							>Password</label
						>
						<div class="relative rounded-md shadow-sm">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<i class="fas fa-lock text-gray-400"></i>
							</div>
							<input
								id="password"
								name="password"
								type="password"
								autocomplete="current-password"
								required
								bind:value={password}
								class="block w-full rounded-lg border border-gray-300 py-3 pl-10 pr-3 transition-all focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 sm:text-sm"
								placeholder="••••••••"
							/>
						</div>
					</div>

					<div class="flex items-center justify-between">
						<div class="flex items-center">
							<input
								id="remember-me"
								name="remember-me"
								type="checkbox"
								class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
							/>
							<label for="remember-me" class="ml-2 block text-sm text-gray-900">Remember me</label>
						</div>

						<div class="text-sm">
							<a href="/forgot-password" class="font-medium text-blue-600 hover:text-blue-500"
								>Forgot password?</a
							>
						</div>
					</div>

					<div>
						<button
							type="submit"
							disabled={loading}
							class="flex w-full transform items-center justify-center rounded-lg border border-transparent bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-3 text-sm font-bold text-white shadow-lg transition-all hover:-translate-y-0.5 hover:from-blue-700 hover:to-purple-700 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
						>
							{#if loading}
								<i class="fas fa-spinner fa-spin mr-2"></i>
								Signing in...
							{:else}
								<i class="fas fa-sign-in-alt mr-2"></i>
								Sign in
							{/if}
						</button>
					</div>
				</form>

				<div class="mt-6">
					<div class="relative">
						<div class="absolute inset-0 flex items-center">
							<div class="w-full border-t border-gray-200"></div>
						</div>
						<div class="relative flex justify-center text-sm">
							<span class="bg-white px-3 text-gray-500">Don't have an account?</span>
						</div>
					</div>

					<div class="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
						<a
							href="/register"
							class="inline-flex w-full items-center justify-center rounded-lg border-2 border-gray-200 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-sm transition-all hover:border-blue-500 hover:text-blue-600 hover:shadow-md"
						>
							<i class="fas fa-user mr-2"></i>
							Register as Driver
						</a>
						<a
							href="/register?role=provider"
							class="inline-flex w-full items-center justify-center rounded-lg border-2 border-gray-200 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 shadow-sm transition-all hover:border-purple-500 hover:text-purple-600 hover:shadow-md"
						>
							<i class="fas fa-tools mr-2"></i>
							Register as Provider
						</a>
					</div>
				</div>
			</div>

			<!-- Back to Home -->
			<div class="text-center">
				<a href="/" class="text-sm text-gray-600 transition-colors hover:text-blue-600">
					<i class="fas fa-arrow-left mr-1"></i>
					Back to Home
				</a>
			</div>
		</div>
	</div>
</div>
