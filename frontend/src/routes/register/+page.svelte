<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { register } from '$lib/stores/auth';

	let firstName = $state('');
	let lastName = $state('');
	let businessName = $state('');
	let email = $state('');
	let phone = $state('');
	let password = $state('');
	let role = $state('driver');
	let loading = $state(false);
	let error = $state('');
	let showPassword = $state(false);

	// Initialize role from URL parameter if present
	if ($page.url.searchParams.get('role') === 'service_provider') {
		role = 'service_provider';
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();

		let validationError = false;
		if (!firstName || !lastName || !email || !phone || !password) validationError = true;
		if (role === 'service_provider' && !businessName) validationError = true;

		if (validationError) {
			error = 'Please fill in all fields';
			return;
		}

		loading = true;
		error = '';

		try {
			const userData = {
				first_name: firstName,
				last_name: lastName,
				email,
				phone,
				password,
				role,
				...(role === 'service_provider' && businessName ? { business_name: businessName } : {})
			};

			const result = await register(userData);

			if (result.success) {
				// Registration successful, redirect to login
				goto('/login?registered=true');
			} else {
				error = result.error || 'Registration failed';
			}
		} catch (e: any) {
			console.error(e);
			error = e.message || 'Registration failed';
		}

		loading = false;
	}
	let gradientClass = $derived(
		role === 'driver'
			? 'bg-gradient-to-br from-cyan-600 to-blue-700'
			: 'bg-gradient-to-br from-purple-600 to-green-600'
	);

	let btnGradientClass = $derived(
		role === 'driver' ? 'from-cyan-600 to-blue-600' : 'from-purple-600 to-green-600'
	);

	let btnHoverClass = $derived(
		role === 'driver'
			? 'hover:from-cyan-700 hover:to-blue-700'
			: 'hover:from-purple-700 hover:to-green-700'
	);

	let ringClass = $derived(role === 'driver' ? 'focus:ring-blue-500' : 'focus:ring-green-500');

	let accentTextClass = $derived(role === 'driver' ? 'text-blue-100' : 'text-green-100');
</script>

<svelte:head>
	<title>Register - VBAMS</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-100 p-4">
	<div class="w-full max-w-6xl overflow-hidden rounded-3xl bg-white shadow-2xl">
		<div class="grid lg:grid-cols-2">
			<!-- Left Panel - Branding -->
			<div
				class="relative flex flex-col justify-center overflow-hidden {gradientClass} p-12 text-white transition-all duration-500"
			>
				<!-- Decorative circles -->
				<div class="absolute left-10 top-10 h-32 w-32 rounded-full bg-white/10"></div>
				<div class="absolute bottom-10 right-10 h-40 w-40 rounded-full bg-white/10"></div>
				<div class="absolute right-20 top-1/2 h-20 w-20 rounded-full bg-blue-400/20"></div>

				<div class="relative z-10">
					<!-- Logo -->
					<div class="mb-8 flex items-center">
						<div class="mr-3 flex h-12 w-12 items-center justify-center rounded-xl bg-white/20">
							<i class="fas fa-user-plus text-2xl"></i>
						</div>
						<span class="text-2xl font-bold">VBAMS</span>
					</div>

					<!-- Title -->
					<h1 class="mb-6 text-4xl font-bold">Join Our Community</h1>

					<!-- Features List -->
					<div class="space-y-6">
						<div class="flex items-start">
							<div
								class="mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-white/20"
							>
								<i class="fas fa-car {accentTextClass}"></i>
							</div>
							<div class="ml-4">
								<h3 class="text-lg font-semibold text-white">For Drivers</h3>
								<p class={accentTextClass}>
									Get immediate roadside assistance anywhere, anytime. Track your provider in
									real-time.
								</p>
							</div>
						</div>

						<div class="flex items-start">
							<div
								class="mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-white/20"
							>
								<i class="fas fa-tools {accentTextClass}"></i>
							</div>
							<div class="ml-4">
								<h3 class="text-lg font-semibold text-white">For Service Providers</h3>
								<p class={accentTextClass}>
									Grow your business, manage service requests efficiently, and get paid securely.
								</p>
							</div>
						</div>
					</div>

					<!-- Trust Badge -->
					<div class="mt-10 rounded-xl bg-white/10 p-4 backdrop-blur-sm">
						<div class="flex items-center space-x-2 text-sm {accentTextClass}">
							<i class="fas fa-shield-alt"></i>
							<span>Secure & Verified Platform</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Right Panel - Register Form -->
			<div class="flex flex-col justify-center p-8 lg:p-12">
				<!-- Back to Home -->
				<a href="/" class="mb-6 inline-flex items-center text-sm text-gray-500 hover:text-gray-700">
					<i class="fas fa-arrow-left mr-2"></i>
					Back to Home
				</a>

				<!-- Header -->
				<div class="mb-8">
					<h2 class="mb-2 text-3xl font-bold text-gray-900">Create Account</h2>
					<p class="text-gray-500">Get started with your free account today</p>
				</div>

				{#if error}
					<div class="mb-6 rounded-xl border-2 border-red-200 bg-red-50 px-4 py-3 text-red-700">
						<i class="fas fa-exclamation-circle mr-2"></i>
						{error}
					</div>
				{/if}

				<!-- Register Form -->
				<form onsubmit={handleSubmit} class="space-y-5">
					<!-- Name Fields -->
					<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
						<div>
							<label for="firstName" class="mb-2 block text-sm font-medium text-gray-700"
								>First Name</label
							>
							<input
								id="firstName"
								type="text"
								bind:value={firstName}
								placeholder="John"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 {ringClass}"
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
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 {ringClass}"
								required
							/>
						</div>
					</div>

					{#if role === 'service_provider'}
						<div>
							<label for="businessName" class="mb-2 block text-sm font-medium text-gray-700"
								>Business / Brand Name</label
							>
							<input
								id="businessName"
								type="text"
								bind:value={businessName}
								placeholder="e.g. Quick Fix Auto"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 {ringClass}"
								required
							/>
						</div>
					{/if}

					<!-- Contact Fields -->
					<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
						<div>
							<label for="email" class="mb-2 block text-sm font-medium text-gray-700"
								>Email Address</label
							>
							<input
								id="email"
								type="email"
								bind:value={email}
								placeholder="john@example.com"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 {ringClass}"
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
								class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 {ringClass}"
								required
							/>
						</div>
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
								placeholder="At least 6 characters"
								class="w-full rounded-xl border border-gray-300 px-4 py-3 pr-10 focus:border-transparent focus:outline-none focus:ring-2 {ringClass}"
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

					<!-- Role Selection -->
					<div>
						<label for="role" class="mb-2 block text-sm font-medium text-gray-700"
							>I am joining to...</label
						>
						<div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
							<label
								class="relative cursor-pointer rounded-xl border p-4 transition-all hover:border-blue-500 peer-checked:border-blue-600 peer-checked:bg-blue-50 {role ===
								'driver'
									? 'border-blue-600 bg-blue-50'
									: 'border-gray-200'}"
							>
								<input type="radio" name="role" value="driver" bind:group={role} class="sr-only" />
								<div class="flex items-center">
									<div
										class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600"
									>
										<i class="fas fa-car"></i>
									</div>
									<div class="ml-3">
										<p class="font-semibold text-gray-900">Get Help</p>
										<p class="text-xs text-gray-500">I'm a Driver</p>
									</div>
									{#if role === 'driver'}
										<i class="fas fa-check-circle ml-auto text-blue-600"></i>
									{/if}
								</div>
							</label>

							<label
								class="relative cursor-pointer rounded-xl border p-4 transition-all hover:border-green-500 peer-checked:border-green-600 peer-checked:bg-green-50 {role ===
								'service_provider'
									? 'border-green-600 bg-green-50'
									: 'border-gray-200'}"
							>
								<input
									type="radio"
									name="role"
									value="service_provider"
									bind:group={role}
									class="sr-only"
								/>
								<div class="flex items-center">
									<div
										class="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-green-600"
									>
										<i class="fas fa-tools"></i>
									</div>
									<div class="ml-3">
										<p class="font-semibold text-gray-900">Offer Service</p>
										<p class="text-xs text-gray-500">I'm a Provider</p>
									</div>
									{#if role === 'service_provider'}
										<i class="fas fa-check-circle ml-auto text-green-600"></i>
									{/if}
								</div>
							</label>
						</div>
					</div>

					<!-- Submit Button -->
					<div class="pt-2">
						<button
							type="submit"
							disabled={loading}
							class="w-full rounded-xl bg-gradient-to-r {btnGradientClass} py-3 font-semibold text-white transition-all {btnHoverClass} disabled:cursor-not-allowed disabled:opacity-50"
						>
							{#if loading}
								<i class="fas fa-spinner fa-spin mr-2"></i>
								Creating Account...
							{:else}
								<i class="fas fa-user-plus mr-2"></i>
								Create Account
							{/if}
						</button>
					</div>

					<!-- Footer -->
					<div class="text-center text-sm text-gray-500">
						Already have an account?
						<a href="/login" class="font-semibold text-blue-600 hover:text-blue-700">Sign in here</a
						>
					</div>
				</form>
			</div>
		</div>
	</div>
</div>
