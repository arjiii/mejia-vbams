<script lang="ts">
	import { fade, fly, scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
</script>

<svelte:head>
	<title>VBAMS - Vehicle Breakdown Assistance Management System</title>
	<meta
		name="description"
		content="Professional roadside assistance platform connecting drivers with verified service providers."
	/>
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
	/>
</svelte:head>

<!-- Navigation -->
<nav class="sticky top-0 z-50 border-b border-gray-200 bg-white bg-white/90 backdrop-blur-sm">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="flex h-16 items-center justify-between">
			<!-- Logo -->
			<div class="animate-slideIn flex items-center">
				<div
					class="mr-3 flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-purple-600 shadow-lg"
				>
					<i class="fas fa-car text-lg text-white"></i>
				</div>
				<span
					class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-xl font-bold text-transparent"
					>VBAMS</span
				>
			</div>

			<!-- Nav Links -->
			<div class="hidden items-center space-x-8 md:flex">
				<a href="#features" class="font-medium text-gray-600 transition-colors hover:text-blue-600"
					>Features</a
				>
				<a
					href="#how-it-works"
					class="font-medium text-gray-600 transition-colors hover:text-purple-600">How It Works</a
				>
				<a href="#about" class="font-medium text-gray-600 transition-colors hover:text-blue-600"
					>About</a
				>
				<a
					href="/login"
					class="transform rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-2 font-medium text-white transition-all hover:-translate-y-0.5 hover:shadow-lg"
				>
					Login
				</a>
			</div>
		</div>
	</div>
</nav>

<!-- Hero Section -->
<section
	class="relative overflow-hidden bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-20"
>
	<!-- Animated Background Blobs -->
	<div class="absolute inset-0 overflow-hidden">
		<div class="blob blob-1"></div>
		<div class="blob blob-2"></div>
		<div class="blob blob-3"></div>
	</div>

	<div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="mx-auto mb-16 max-w-3xl text-center">
			<h1 class="animate-fadeInUp mb-6 text-5xl font-bold leading-tight text-gray-900 md:text-6xl">
				Roadside Assistance,<br />
				<span
					class="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent"
				>
					Made Simple
				</span>
			</h1>
			<p class="animate-fadeInUp animation-delay-200 mb-10 text-xl text-gray-600">
				Connect with verified service providers instantly. Get help when you need it most.
			</p>
		</div>

		<!-- Login Cards -->
		<div class="mx-auto grid max-w-5xl grid-cols-1 gap-6 md:grid-cols-3">
			<!-- Driver Card -->
			<a
				href="/login/driver"
				class="animate-fadeInUp group block transform rounded-2xl border-2 border-blue-200 bg-white p-8 transition-all hover:-translate-y-2 hover:border-blue-600 hover:shadow-2xl"
			>
				<div class="flex flex-col items-center text-center">
					<div
						class="mb-4 flex h-16 w-16 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg transition-transform group-hover:scale-110"
					>
						<i class="fas fa-car text-2xl text-white"></i>
					</div>
					<h3 class="mb-2 text-xl font-bold text-gray-900">I'm a Driver</h3>
					<p class="mb-6 text-sm text-gray-600">Get roadside assistance instantly</p>
					<div
						class="w-full rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 py-3 font-semibold text-white transition-all group-hover:shadow-lg"
					>
						Login
					</div>
				</div>
			</a>

			<!-- Service Provider Card -->
			<a
				href="/login/provider"
				class="animate-fadeInUp animation-delay-100 group block transform rounded-2xl border-2 border-purple-200 bg-white p-8 transition-all hover:-translate-y-2 hover:border-purple-600 hover:shadow-2xl"
			>
				<div class="flex flex-col items-center text-center">
					<div
						class="mb-4 flex h-16 w-16 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 shadow-lg transition-transform group-hover:scale-110"
					>
						<i class="fas fa-tools text-2xl text-white"></i>
					</div>
					<h3 class="mb-2 text-xl font-bold text-gray-900">I'm a Provider</h3>
					<p class="mb-6 text-sm text-gray-600">Grow your service business</p>
					<div
						class="w-full rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 py-3 font-semibold text-white transition-all group-hover:shadow-lg"
					>
						Login
					</div>
				</div>
			</a>

			<!-- Admin Card -->
			<a
				href="/login/admin"
				class="animate-fadeInUp animation-delay-200 group block transform rounded-2xl border-2 border-red-200 bg-white p-8 transition-all hover:-translate-y-2 hover:border-red-600 hover:shadow-2xl"
			>
				<div class="flex flex-col items-center text-center">
					<div
						class="mb-4 flex h-16 w-16 items-center justify-center rounded-xl bg-gradient-to-br from-red-500 to-orange-500 shadow-lg transition-transform group-hover:scale-110"
					>
						<i class="fas fa-shield-alt text-2xl text-white"></i>
					</div>
					<h3 class="mb-2 text-xl font-bold text-gray-900">Administrator</h3>
					<p class="mb-6 text-sm text-gray-600">Manage the platform</p>
					<div
						class="w-full rounded-xl bg-gradient-to-r from-red-600 to-orange-600 py-3 font-semibold text-white transition-all group-hover:shadow-lg"
					>
						Login
					</div>
				</div>
			</a>
		</div>
	</div>
</section>

<!-- Features Section -->
<section id="features" class="bg-white py-20">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="mb-16 text-center">
			<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">Why Choose VBAMS</h2>
			<p class="text-lg text-gray-600">Professional roadside assistance platform</p>
		</div>

		<div class="grid grid-cols-1 gap-12 md:grid-cols-3">
			<div class="hover-lift group text-center">
				<div
					class="mx-auto mb-4 flex h-20 w-20 transform items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg transition-transform group-hover:rotate-6"
				>
					<i class="fas fa-bolt text-3xl text-white"></i>
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">Fast Response</h3>
				<p class="text-gray-600">Get connected with service providers in under 60 seconds</p>
			</div>

			<div class="hover-lift animation-delay-100 group text-center">
				<div
					class="mx-auto mb-4 flex h-20 w-20 transform items-center justify-center rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 shadow-lg transition-transform group-hover:rotate-6"
				>
					<i class="fas fa-shield-check text-3xl text-white"></i>
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">Verified Providers</h3>
				<p class="text-gray-600">All service providers are thoroughly vetted and verified</p>
			</div>

			<div class="hover-lift animation-delay-200 group text-center">
				<div
					class="mx-auto mb-4 flex h-20 w-20 transform items-center justify-center rounded-2xl bg-gradient-to-br from-green-500 to-emerald-500 shadow-lg transition-transform group-hover:rotate-6"
				>
					<i class="fas fa-map-marked-alt text-3xl text-white"></i>
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">Real-Time Tracking</h3>
				<p class="text-gray-600">Track your service provider's location in real-time</p>
			</div>
		</div>
	</div>
</section>

<!-- How It Works Section -->
<section id="how-it-works" class="bg-gradient-to-br from-gray-50 to-blue-50 py-20">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="mb-16 text-center">
			<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">How It Works</h2>
			<p class="text-lg text-gray-600">Get assistance in three simple steps</p>
		</div>

		<div class="relative grid grid-cols-1 gap-8 md:grid-cols-3">
			<!-- Connection Lines (Desktop) -->
			<div
				class="absolute left-1/4 right-1/4 top-8 hidden h-1 bg-gradient-to-r from-blue-300 via-purple-300 to-pink-300 md:block"
			></div>

			<div class="hover-lift group relative text-center">
				<div
					class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-cyan-600 text-2xl font-bold text-white shadow-lg transition-transform group-hover:scale-110"
				>
					1
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">Request Assistance</h3>
				<p class="text-gray-600">Submit your breakdown details and location</p>
			</div>

			<div class="hover-lift animation-delay-100 group relative text-center">
				<div
					class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-purple-600 to-pink-600 text-2xl font-bold text-white shadow-lg transition-transform group-hover:scale-110"
				>
					2
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">Get Matched</h3>
				<p class="text-gray-600">We connect you with the nearest available provider</p>
			</div>

			<div class="hover-lift animation-delay-200 group relative text-center">
				<div
					class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-green-600 to-emerald-600 text-2xl font-bold text-white shadow-lg transition-transform group-hover:scale-110"
				>
					3
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">Get Help</h3>
				<p class="text-gray-600">Track arrival and receive professional service</p>
			</div>
		</div>
	</div>
</section>

<!-- Stats Section -->
<section class="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 py-16">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="grid grid-cols-2 gap-8 text-center text-white md:grid-cols-4">
			<div class="stat-item">
				<div class="counter mb-2 text-5xl font-bold">10,000+</div>
				<div class="text-blue-100">Active Users</div>
			</div>
			<div class="stat-item animation-delay-100">
				<div class="counter mb-2 text-5xl font-bold">500+</div>
				<div class="text-purple-100">Service Providers</div>
			</div>
			<div class="stat-item animation-delay-200">
				<div class="counter mb-2 text-5xl font-bold">50,000+</div>
				<div class="text-pink-100">Jobs Completed</div>
			</div>
			<div class="stat-item animation-delay-300">
				<div class="counter mb-2 text-5xl font-bold">4.9/5</div>
				<div class="text-blue-100">Average Rating</div>
			</div>
		</div>
	</div>
</section>

<!-- About Section -->
<section id="about" class="bg-white py-20">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="mx-auto max-w-3xl text-center">
			<h2 class="mb-6 text-3xl font-bold text-gray-900 md:text-4xl">About VBAMS</h2>
			<p class="mb-8 text-lg leading-relaxed text-gray-600">
				Vehicle Breakdown Assistance Management System (VBAMS) is a professional platform connecting
				drivers with verified service providers. We leverage technology to make roadside assistance
				fast, reliable, and transparent.
			</p>
			<div class="mt-12 grid grid-cols-1 gap-6 md:grid-cols-3">
				<div
					class="hover-lift rounded-xl border-2 border-blue-200 p-6 transition-all hover:border-blue-600 hover:shadow-lg"
				>
					<i
						class="fas fa-clock mb-3 bg-gradient-to-br from-blue-600 to-cyan-600 bg-clip-text text-4xl text-transparent"
					></i>
					<h4 class="mb-2 font-bold text-gray-900">24/7 Availability</h4>
					<p class="text-sm text-gray-600">Always here when you need us</p>
				</div>
				<div
					class="hover-lift animation-delay-100 rounded-xl border-2 border-purple-200 p-6 transition-all hover:border-purple-600 hover:shadow-lg"
				>
					<i
						class="fas fa-dollar-sign mb-3 bg-gradient-to-br from-purple-600 to-pink-600 bg-clip-text text-4xl text-transparent"
					></i>
					<h4 class="mb-2 font-bold text-gray-900">Transparent Pricing</h4>
					<p class="text-sm text-gray-600">No hidden fees or surprises</p>
				</div>
				<div
					class="hover-lift animation-delay-200 rounded-xl border-2 border-green-200 p-6 transition-all hover:border-green-600 hover:shadow-lg"
				>
					<i
						class="fas fa-headset mb-3 bg-gradient-to-br from-green-600 to-emerald-600 bg-clip-text text-4xl text-transparent"
					></i>
					<h4 class="mb-2 font-bold text-gray-900">Dedicated Support</h4>
					<p class="text-sm text-gray-600">Professional customer service</p>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- CTA Section -->
<section class="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-20">
	<div class="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
		<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">Ready to Get Started?</h2>
		<p class="mb-8 text-lg text-gray-600">Choose your role and access the platform</p>
		<div class="flex flex-col justify-center gap-4 sm:flex-row">
			<a
				href="/login/driver"
				class="transform rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 px-8 py-4 font-semibold text-white transition-all hover:-translate-y-1 hover:shadow-2xl"
			>
				<i class="fas fa-car mr-2"></i>
				Login as Driver
			</a>
			<a
				href="/login/provider"
				class="transform rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 font-semibold text-white transition-all hover:-translate-y-1 hover:shadow-2xl"
			>
				<i class="fas fa-tools mr-2"></i>
				Login as Provider
			</a>
		</div>
	</div>
</section>

<!-- Footer -->
<footer class="bg-gray-900 py-12 text-white">
	<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<div class="grid grid-cols-1 gap-8 md:grid-cols-4">
			<!-- Brand -->
			<div class="col-span-1 md:col-span-2">
				<div class="mb-4 flex items-center">
					<div
						class="mr-3 flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-purple-600"
					>
						<i class="fas fa-car text-white"></i>
					</div>
					<span class="text-xl font-bold">VBAMS</span>
				</div>
				<p class="max-w-sm text-gray-400">
					Professional roadside assistance platform connecting drivers with verified service
					providers.
				</p>
			</div>

			<!-- Quick Links -->
			<div>
				<h3 class="mb-4 font-bold">Access Portal</h3>
				<ul class="space-y-2">
					<li>
						<a href="/login/driver" class="text-gray-400 transition-colors hover:text-blue-400"
							>Driver Login</a
						>
					</li>
					<li>
						<a href="/login/provider" class="text-gray-400 transition-colors hover:text-purple-400"
							>Provider Login</a
						>
					</li>
					<li>
						<a href="/login/admin" class="text-gray-400 transition-colors hover:text-red-400"
							>Admin Login</a
						>
					</li>
				</ul>
			</div>

			<!-- Contact -->
			<div>
				<h3 class="mb-4 font-bold">Contact</h3>
				<ul class="space-y-2 text-gray-400">
					<li class="flex items-center transition-colors hover:text-white">
						<i class="fas fa-envelope mr-2 text-sm"></i>
						<span class="text-sm">support@vbams.com</span>
					</li>
					<li class="flex items-center transition-colors hover:text-white">
						<i class="fas fa-phone mr-2 text-sm"></i>
						<span class="text-sm">+1 (555) 123-4567</span>
					</li>
					<li class="flex items-center transition-colors hover:text-white">
						<i class="fas fa-clock mr-2 text-sm"></i>
						<span class="text-sm">24/7 Support</span>
					</li>
				</ul>
			</div>
		</div>

		<div class="mt-12 border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
			&copy; {new Date().getFullYear()} VBAMS. All rights reserved.
		</div>
	</div>
</footer>

<style>
	/* Animated Background Blobs */
	.blob {
		position: absolute;
		border-radius: 50%;
		filter: blur(70px);
		opacity: 0.5;
		animation: blob 20s infinite;
	}

	.blob-1 {
		width: 300px;
		height: 300px;
		background: linear-gradient(to right, #3b82f6, #8b5cf6);
		top: -100px;
		left: -100px;
	}

	.blob-2 {
		width: 400px;
		height: 400px;
		background: linear-gradient(to right, #8b5cf6, #ec4899);
		bottom: -150px;
		right: -150px;
		animation-delay: -10s;
	}

	.blob-3 {
		width: 250px;
		height: 250px;
		background: linear-gradient(to right, #06b6d4, #3b82f6);
		top: 50%;
		left: 50%;
		animation-delay: -5s;
	}

	@keyframes blob {
		0%,
		100% {
			transform: translate(0, 0) scale(1);
		}
		33% {
			transform: translate(30px, -50px) scale(1.1);
		}
		66% {
			transform: translate(-20px, 20px) scale(0.9);
		}
	}

	/* Fade in up animation */
	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.animate-fadeInUp {
		animation: fadeInUp 0.6s ease-out forwards;
		opacity: 0;
	}

	.animation-delay-100 {
		animation-delay: 0.1s;
	}

	.animation-delay-200 {
		animation-delay: 0.2s;
	}

	.animation-delay-300 {
		animation-delay: 0.3s;
	}

	/* Slide in animation */
	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.animate-slideIn {
		animation: slideIn 0.5s ease-out;
	}

	/* Hover lift effect */
	.hover-lift {
		transition:
			transform 0.3s ease,
			box-shadow 0.3s ease;
	}

	.hover-lift:hover {
		transform: translateY(-8px);
	}

	/* Stats counter animation */
	.stat-item {
		animation: fadeInUp 0.8s ease-out forwards;
		opacity: 0;
	}

	.counter {
		display: inline-block;
		animation: counterScale 0.6s ease-out 0.3s forwards;
		transform: scale(0);
	}

	@keyframes counterScale {
		0% {
			transform: scale(0);
		}
		50% {
			transform: scale(1.1);
		}
		100% {
			transform: scale(1);
		}
	}
</style>
