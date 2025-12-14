<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, fly, slide } from 'svelte/transition';

	let mobileMenuOpen = false;
	let innerWidth: number;
	let scrollY: number;

	function toggleMobileMenu() {
		mobileMenuOpen = !mobileMenuOpen;
	}

	function closeMobileMenu() {
		mobileMenuOpen = false;
	}
</script>

<svelte:window bind:innerWidth bind:scrollY />

<svelte:head>
	<title>VBAMS - Professional Roadside Assistance</title>
	<meta
		name="description"
		content="Fast, reliable vehicle breakdown assistance connecting drivers with verified service providers."
	/>
	<!-- Font Awesome -->
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
	/>
	<!-- Google Fonts -->
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link
		href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div
	class="min-h-screen bg-gray-50 font-sans text-gray-900 selection:bg-blue-100 selection:text-blue-900"
>
	<!-- Navbar -->
	<nav
		class={`fixed left-0 right-0 top-0 z-50 transition-all duration-300 ${
			scrollY > 20 ? 'bg-white/90 shadow-sm backdrop-blur-md' : 'bg-transparent'
		}`}
	>
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="flex h-20 items-center justify-between">
				<!-- Logo -->
				<div class="flex items-center gap-3">
					<div
						class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 text-white shadow-lg"
					>
						<i class="fas fa-car-crash text-lg"></i>
					</div>
					<span
						class="bg-gradient-to-r from-blue-700 to-purple-700 bg-clip-text text-xl font-extrabold tracking-tight text-transparent"
					>
						VBAMS
					</span>
				</div>

				<!-- Desktop Menu -->
				<div class="hidden items-center space-x-8 md:flex">
					<a
						href="#how-it-works"
						class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
						>How it Works</a
					>
					<a
						href="#features"
						class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
						>Features</a
					>
					<a
						href="#roles"
						class="text-sm font-medium text-gray-600 transition-colors hover:text-blue-600"
						>For Providers</a
					>
					<div class="flex items-center gap-3 border-l border-gray-200 pl-4">
						<a href="/login" class="text-sm font-semibold text-gray-700 hover:text-blue-600"
							>Log in</a
						>
						<a
							href="/register"
							class="rounded-full bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-md transition-all hover:bg-blue-700 hover:shadow-lg focus:ring-4 focus:ring-blue-100"
						>
							Get Started
						</a>
					</div>
				</div>

				<!-- Mobile Hamburger -->
				<div class="flex md:hidden">
					<button
						onclick={toggleMobileMenu}
						class="rounded-md p-2 text-gray-600 hover:bg-gray-100 focus:outline-none"
						aria-label="Toggle menu"
					>
						<i class={`fas ${mobileMenuOpen ? 'fa-times' : 'fa-bars'} text-xl`}></i>
					</button>
				</div>
			</div>
		</div>

		<!-- Mobile Menu Dropdown -->
		{#if mobileMenuOpen}
			<div
				transition:slide={{ duration: 200 }}
				class="border-b border-gray-100 bg-white shadow-xl md:hidden"
			>
				<div class="space-y-1 px-4 py-4 pb-6">
					<a
						href="#how-it-works"
						onclick={closeMobileMenu}
						class="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-blue-600"
					>
						How it Works
					</a>
					<a
						href="#features"
						onclick={closeMobileMenu}
						class="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-blue-600"
					>
						Features
					</a>
					<a
						href="#roles"
						onclick={closeMobileMenu}
						class="block rounded-lg px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-blue-600"
					>
						For Providers
					</a>
					<div class="mt-4 grid grid-cols-2 gap-3 border-t border-gray-100 pt-4">
						<a
							href="/login"
							onclick={closeMobileMenu}
							class="flex items-center justify-center rounded-lg border border-gray-300 px-4 py-2.5 text-center font-semibold text-gray-700 hover:bg-gray-50"
						>
							Log in
						</a>
						<a
							href="/register"
							onclick={closeMobileMenu}
							class="flex items-center justify-center rounded-lg bg-blue-600 px-4 py-2.5 text-center font-semibold text-white hover:bg-blue-700"
						>
							Sign up
						</a>
					</div>
				</div>
			</div>
		{/if}
	</nav>

	<!-- Hero Section -->
	<header class="relative overflow-hidden pb-20 pt-32 lg:pb-32 lg:pt-48">
		<!-- Background Elements -->
		<div
			class="absolute -right-24 -top-24 h-96 w-96 rounded-full bg-blue-200/50 blur-3xl filter"
		></div>
		<div
			class="absolute -left-24 top-1/2 h-72 w-72 rounded-full bg-purple-200/50 blur-3xl filter"
		></div>

		<div class="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="items-center lg:grid lg:grid-cols-12 lg:gap-16">
				<!-- Text Content -->
				<div class="mb-12 text-center lg:col-span-7 lg:mb-0 lg:text-left">
					<div
						class="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-blue-700"
					>
						<span class="h-2 w-2 animate-pulse rounded-full bg-blue-500"></span>
						24/7 Assistance
					</div>
					<h1
						class="mb-6 text-4xl font-extrabold leading-tight tracking-tight text-gray-900 sm:text-5xl md:text-6xl"
					>
						Roadside help when <br class="hidden lg:block" />
						<span
							class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
						>
							you need it most.
						</span>
					</h1>
					<p class="mx-auto mb-8 max-w-2xl text-lg leading-relaxed text-gray-600 lg:mx-0">
						Instant connection to verified mechanics and tow trucks. Track your help in real-time.
						No membership fees, pay only when you use it.
					</p>

					<div class="flex flex-col items-center justify-center gap-4 sm:flex-row lg:justify-start">
						<a
							href="/login"
							class="inline-flex w-full items-center justify-center rounded-full bg-blue-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-blue-600/30 transition-all hover:-translate-y-0.5 hover:bg-blue-700 sm:w-auto"
						>
							Request Assistance
							<i class="fas fa-arrow-right ml-2"></i>
						</a>
						<a
							href="#how-it-works"
							class="inline-flex w-full items-center justify-center rounded-full border border-gray-300 bg-white px-8 py-3.5 text-base font-semibold text-gray-700 transition-all hover:border-gray-400 hover:bg-gray-50 sm:w-auto"
						>
							How it works
						</a>
					</div>
				</div>

				<!-- Hero Visual -->
				<div class="relative lg:col-span-5">
					<div class="relative mx-auto w-full max-w-md lg:max-w-full">
						<!-- Main Card -->
						<div class="relative z-10 rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-gray-900/5">
							<div class="mb-6 flex items-center justify-between">
								<div>
									<h3 class="font-bold text-gray-900">Arriving Soon</h3>
									<p class="text-sm text-gray-500">Tow Truck • 5 mins away</p>
								</div>
								<div
									class="flex h-10 w-10 items-center justify-center rounded-full bg-green-100 text-green-600"
								>
									<i class="fas fa-phone"></i>
								</div>
							</div>

							<!-- Map Placeholder -->
							<div
								class="relative mb-4 flex h-48 w-full items-center justify-center overflow-hidden rounded-xl bg-gray-100"
							>
								<div
									class="absolute inset-0 opacity-20"
									style="background-image: radial-gradient(#cbd5e1 2px, transparent 2px); background-size: 20px 20px;"
								></div>
								<div class="relative z-10 animate-bounce">
									<i class="fas fa-map-marker-alt text-4xl text-blue-600 drop-shadow-lg"></i>
								</div>
							</div>

							<!-- Driver Info -->
							<div class="flex items-center">
								<div
									class="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full border-2 border-white bg-gray-200 shadow-sm"
								>
									<img
										src="https://ui-avatars.com/api/?name=John+D&background=random"
										alt="Driver"
									/>
								</div>
								<div class="ml-3">
									<p class="text-sm font-semibold text-gray-900">John Best</p>
									<div class="flex items-center text-xs text-yellow-500">
										<i class="fas fa-star"></i>
										<span class="ml-1 text-gray-600">4.9 (120+ jobs)</span>
									</div>
								</div>
							</div>
						</div>

						<!-- Floating Badge 1 -->
						<div
							class="animate-float-slow absolute -right-6 -top-6 z-0 hidden rounded-xl bg-white p-3 shadow-xl ring-1 ring-gray-900/5 sm:block lg:-right-12"
						>
							<div class="flex items-center gap-3">
								<div class="rounded-lg bg-green-100 p-2 text-green-600">
									<i class="fas fa-check"></i>
								</div>
								<div>
									<div class="text-xs text-gray-500">Assistance</div>
									<div class="text-sm font-bold">Verified</div>
								</div>
							</div>
						</div>

						<!-- Floating Badge 2 -->
						<div
							class="animate-float-delayed absolute -bottom-6 -left-6 z-20 hidden rounded-xl bg-white p-3 shadow-xl ring-1 ring-gray-900/5 sm:block"
						>
							<div class="flex items-center gap-3">
								<div class="rounded-lg bg-purple-100 p-2 text-purple-600">
									<i class="fas fa-bolt"></i>
								</div>
								<div>
									<div class="text-xs text-gray-500">Response Time</div>
									<div class="text-sm font-bold">&lt; 15 mins</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</header>

	<!-- How it works Section -->
	<section id="how-it-works" class="bg-blue-50 py-20">
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="mb-16 text-center">
				<h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">How VBAMS Works</h2>
				<p class="mt-4 text-lg text-gray-600">Getting back on the road is as easy as 1-2-3.</p>
			</div>

			<div class="relative grid grid-cols-1 gap-8 md:grid-cols-3">
				<!-- Step 1 -->
				<div class="relative flex flex-col items-center text-center">
					<div
						class="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-2xl font-bold text-white shadow-lg shadow-blue-600/30"
					>
						1
					</div>
					<h3 class="mb-3 text-xl font-bold text-gray-900">Request Help</h3>
					<p class="max-w-xs text-gray-600">
						Tell us what happened and where you are using our simple app. No signup required to view
						estimates.
					</p>
				</div>

				<!-- Connector Line (Desktop) -->
				<div
					class="absolute left-1/3 top-8 hidden h-0.5 w-1/3 -translate-x-1/2 bg-gray-300 md:block"
				></div>
				<div
					class="absolute right-1/3 top-8 hidden h-0.5 w-1/3 translate-x-1/2 bg-gray-300 md:block"
				></div>

				<!-- Step 2 -->
				<div class="relative flex flex-col items-center text-center">
					<div
						class="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-white text-2xl font-bold text-blue-600 shadow-lg ring-2 ring-blue-600"
					>
						2
					</div>
					<h3 class="mb-3 text-xl font-bold text-gray-900">Get Matched</h3>
					<p class="max-w-xs text-gray-600">
						We instantly notify nearby verified mechanics and tow trucks. Review their profile and
						price.
					</p>
				</div>

				<!-- Step 3 -->
				<div class="relative flex flex-col items-center text-center">
					<div
						class="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-2xl font-bold text-white shadow-lg shadow-blue-600/30"
					>
						3
					</div>
					<h3 class="mb-3 text-xl font-bold text-gray-900">Help Arrives</h3>
					<p class="max-w-xs text-gray-600">
						Track your provider in real-time. Pay securely through the app only after the job is
						done.
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Role Selection Section (Replaces the login shortcuts in a nicer way) -->
	<section id="roles" class="bg-white py-20">
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="mb-16 text-center">
				<h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
					Choose your path
				</h2>
				<p class="mt-4 text-lg text-gray-600">
					Whether you need help or want to provide it, we have the tools for you.
				</p>
			</div>

			<div class="mx-auto grid max-w-4xl grid-cols-1 gap-8 md:grid-cols-2">
				<!-- Driver Card -->
				<a
					href="/login?role=driver"
					class="group relative rounded-3xl border border-gray-200 bg-white p-8 shadow-sm transition-all hover:scale-[1.02] hover:border-blue-200 hover:shadow-xl"
				>
					<div
						class="absolute right-0 top-0 p-6 opacity-10 transition-opacity group-hover:opacity-20"
					>
						<i class="fas fa-car text-8xl text-blue-600"></i>
					</div>
					<div class="relative z-10">
						<div
							class="mb-6 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-blue-600"
						>
							<i class="fas fa-steering-wheel text-xl"></i>
						</div>
						<h3 class="mb-3 text-2xl font-bold text-gray-900">For Drivers</h3>
						<p class="mb-6 text-gray-600">
							Standard vehicle owners. Request assistance, track service providers, and manage your
							vehicles.
						</p>
						<span
							class="inline-flex items-center font-semibold text-blue-600 transition-transform group-hover:translate-x-1"
						>
							Login as Driver <i class="fas fa-arrow-right ml-2 text-sm"></i>
						</span>
					</div>
				</a>

				<!-- Provider Card -->
				<a
					href="/login?role=provider"
					class="group relative rounded-3xl border border-gray-200 bg-white p-8 shadow-sm transition-all hover:scale-[1.02] hover:border-purple-200 hover:shadow-xl"
				>
					<div
						class="absolute right-0 top-0 p-6 opacity-10 transition-opacity group-hover:opacity-20"
					>
						<i class="fas fa-tools text-8xl text-purple-600"></i>
					</div>
					<div class="relative z-10">
						<div
							class="mb-6 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-purple-100 text-purple-600"
						>
							<i class="fas fa-wrench text-xl"></i>
						</div>
						<h3 class="mb-3 text-2xl font-bold text-gray-900">For Providers</h3>
						<p class="mb-6 text-gray-600">
							Mechanics, tow trucks, and technicians. Accept jobs, manage your schedule, and earn
							money.
						</p>
						<span
							class="inline-flex items-center font-semibold text-purple-600 transition-transform group-hover:translate-x-1"
						>
							Login as Provider <i class="fas fa-arrow-right ml-2 text-sm"></i>
						</span>
					</div>
				</a>
			</div>

			<div class="mt-8 text-center">
				<a
					href="/login/admin"
					class="text-sm font-medium text-gray-500 transition-colors hover:text-gray-800"
				>
					<i class="fas fa-lock mr-1"></i> Admin Access
				</a>
			</div>
		</div>
	</section>

	<!-- Features Grid -->
	<section id="features" class="bg-gray-50/50 py-20">
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="mb-16 text-center">
				<h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
					Everything you need
				</h2>
			</div>

			<div class="grid grid-cols-1 gap-8 md:grid-cols-3">
				<div class="rounded-2xl border border-gray-100 bg-white p-8 shadow-sm">
					<div
						class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-red-100 text-red-600"
					>
						<i class="fas fa-map-marked-alt text-xl"></i>
					</div>
					<h3 class="mb-3 text-xl font-bold text-gray-900">Live Tracking</h3>
					<p class="text-gray-600">
						Watch your service provider approach on the map in real-time. No more guessing.
					</p>
				</div>
				<div class="rounded-2xl border border-gray-100 bg-white p-8 shadow-sm">
					<div
						class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-green-100 text-green-600"
					>
						<i class="fas fa-shield-alt text-xl"></i>
					</div>
					<h3 class="mb-3 text-xl font-bold text-gray-900">Verified Pros</h3>
					<p class="text-gray-600">
						Every mechanic and driver is background checked and verified for your safety.
					</p>
				</div>
				<div class="rounded-2xl border border-gray-100 bg-white p-8 shadow-sm">
					<div
						class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-600"
					>
						<i class="fas fa-receipt text-xl"></i>
					</div>
					<h3 class="mb-3 text-xl font-bold text-gray-900">Transparent Cost</h3>
					<p class="text-gray-600">
						See the estimated cost before you confirm. Secure payment processing.
					</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Footer -->
	<footer class="bg-gray-900 py-12 text-white">
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="mb-8 grid grid-cols-1 gap-8 md:grid-cols-4">
				<div class="col-span-1 md:col-span-2">
					<span
						class="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-2xl font-bold text-transparent"
						>VBAMS</span
					>
					<p class="mt-4 max-w-xs text-gray-400">
						Modernizing roadside assistance for everyone. Fast, safe, and reliable.
					</p>
				</div>
				<div>
					<h4 class="mb-4 font-bold">Platform</h4>
					<ul class="space-y-2 text-sm text-gray-400">
						<li><a href="/login" class="hover:text-white">Login</a></li>
						<li><a href="/register" class="hover:text-white">Register</a></li>
						<li><a href="/about" class="hover:text-white">About Us</a></li>
					</ul>
				</div>
				<div>
					<h4 class="mb-4 font-bold">Support</h4>
					<ul class="space-y-2 text-sm text-gray-400">
						<li><a href="/contact" class="hover:text-white">Contact Center</a></li>
						<li><a href="/faq" class="hover:text-white">FAQ</a></li>
						<li><a href="/privacy" class="hover:text-white">Privacy Policy</a></li>
					</ul>
				</div>
			</div>
			<div class="border-t border-gray-800 pt-8 text-center text-sm text-gray-500">
				&copy; {new Date().getFullYear()} VBAMS. All rights reserved.
			</div>
		</div>
	</footer>
</div>

<style>
	@keyframes float-slow {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-10px);
		}
	}
	@keyframes float-delayed {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-8px);
		}
	}
	.animate-float-slow {
		animation: float-slow 3s ease-in-out infinite;
	}
	.animate-float-delayed {
		animation: float-delayed 4s ease-in-out infinite 1s;
	}
</style>
