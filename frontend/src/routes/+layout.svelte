<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { isAuthenticated, user, logout } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import '../app.css';

	let { children } = $props();

	let showMobileMenu = $state(false);

	// Check if current page is a public page (landing or login pages)
	let isPublicPage = $derived(
		$page.url.pathname === '/' ||
			$page.url.pathname.startsWith('/login') ||
			$page.url.pathname.startsWith('/register') ||
			$page.url.pathname.startsWith('/forgot-password')
	);

	// Only show dashboard layout if authenticated AND not on a public page
	// Reverted to original logic (removed /app exclusion)
	let showDashboardLayout = $derived($isAuthenticated && !isPublicPage);

	function toggleMobileMenu() {
		showMobileMenu = !showMobileMenu;
	}

	function handleLogout() {
		logout();
		showMobileMenu = false;
		goto('/login');
	}

	const roleThemes = {
		admin: {
			sidebar: 'bg-gradient-to-br from-orange-600 to-red-700',
			navItemHover: 'hover:bg-red-800 hover:text-white',
			navItemActive: 'bg-red-800 text-white',
			borderTop: 'border-red-800',
			mobileHeader: 'bg-gradient-to-br from-orange-600 to-red-700'
		},
		service_provider: {
			sidebar: 'bg-gradient-to-br from-green-600 to-emerald-700',
			navItemHover: 'hover:bg-green-800 hover:text-white',
			navItemActive: 'bg-green-800 text-white',
			borderTop: 'border-green-800',
			mobileHeader: 'bg-gradient-to-br from-green-600 to-emerald-700'
		},
		driver: {
			sidebar: 'bg-gradient-to-br from-cyan-600 to-blue-700',
			navItemHover: 'hover:bg-blue-800 hover:text-white',
			navItemActive: 'bg-blue-800 text-white',
			borderTop: 'border-blue-800',
			mobileHeader: 'bg-gradient-to-br from-cyan-600 to-blue-700'
		}
	};

	let currentTheme = $derived(
		roleThemes[$user?.role as keyof typeof roleThemes] || roleThemes.driver
	);
</script>

<svelte:head>
	<title>VBAMS - Vehicle Breakdown Assistance Management System</title>
	<meta
		name="description"
		content="Get instant help when your vehicle breaks down. AI-powered system connects you with nearby service providers."
	/>
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
	/>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	{#if showDashboardLayout}
		<!-- Authenticated Layout -->
		<div class="flex h-screen">
			<!-- Sidebar -->
			<div class="hidden md:flex md:w-64 md:flex-col">
				<div class="flex flex-grow flex-col overflow-y-auto pt-5 {currentTheme.sidebar}">
					<div class="flex flex-shrink-0 items-center px-4">
						<i class="fas fa-car-crash mr-2 text-2xl text-white"></i>
						<span class="text-xl font-bold text-white">VBAMS</span>
					</div>
					<div class="mt-5 flex flex-grow flex-col">
						<nav class="flex-1 space-y-1 px-2">
							<!-- Common for all roles -->
							<a
								href="/dashboard"
								class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
									.url.pathname === '/dashboard'
									? currentTheme.navItemActive
									: ''}"
							>
								<i class="fas fa-tachometer-alt mr-3"></i>
								Dashboard
							</a>

							{#if $user?.role === 'admin'}
								<!-- Admin-specific menu -->
								<a
									href="/admin/users"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page.url.pathname.startsWith(
										'/admin/users'
									)
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-users mr-3"></i>
									Manage Users
								</a>
								<a
									href="/admin/providers"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page.url.pathname.startsWith(
										'/admin/providers'
									)
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-user-cog mr-3"></i>
									Manage Providers
								</a>
								<a
									href="/admin/reports"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page.url.pathname.startsWith(
										'/admin/reports'
									)
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-chart-bar mr-3"></i>
									Reports
								</a>
								<a
									href="/admin/settings"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page.url.pathname.startsWith(
										'/admin/settings'
									)
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-cog mr-3"></i>
									Settings
								</a>
							{:else if $user?.role === 'service_provider'}
								<!-- Service Provider-specific menu -->
								<a
									href="/jobs"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/jobs'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-briefcase mr-3"></i>
									My Jobs
								</a>
								<a
									href="/requests"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/requests'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-bell mr-3"></i>
									Service Requests
								</a>
								<a
									href="/earnings"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/earnings'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-dollar-sign mr-3"></i>
									Earnings
								</a>
								<a
									href="/availability"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/availability'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-calendar-check mr-3"></i>
									Availability
								</a>
							{:else}
								<!-- Driver-specific menu -->
								<a
									href="/vehicles"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/vehicles'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-car mr-3"></i>
									My Vehicles
								</a>
								<a
									href="/breakdowns"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/breakdowns'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-exclamation-triangle mr-3"></i>
									Breakdowns
								</a>
								<a
									href="/assistance"
									class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
										.url.pathname === '/assistance'
										? currentTheme.navItemActive
										: ''}"
								>
									<i class="fas fa-handshake mr-3"></i>
									Assistance
								</a>
							{/if}

							<!-- Common for all roles -->
							<!-- Profile Link (Conditional Name) -->
							<a
								href="/profile"
								class="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-blue-100 {currentTheme.navItemHover} {$page
									.url.pathname === '/profile'
									? currentTheme.navItemActive
									: ''}"
							>
								<i class="fas fa-user mr-3"></i>
								Profile
							</a>
						</nav>
					</div>
					<div class="flex flex-shrink-0 border-t {currentTheme.borderTop} p-4">
						<div class="flex items-center">
							<div class="ml-3">
								<p class="text-sm font-medium text-white">
									{#if $user}
										{$user.first_name} {$user.last_name}
									{/if}
								</p>
								<button onclick={handleLogout} class="text-xs text-blue-200 hover:text-white">
									<i class="fas fa-sign-out-alt mr-1"></i>
									Sign out
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Mobile sidebar -->
			{#if showMobileMenu}
				<div class="md:hidden">
					<div class="fixed inset-0 z-40 flex">
						<div
							class="fixed inset-0 bg-gray-600 bg-opacity-75"
							onclick={toggleMobileMenu}
							aria-hidden="true"
						></div>
						<div class="relative flex w-full max-w-xs flex-1 flex-col {currentTheme.mobileHeader}">
							<div class="absolute right-0 top-0 -mr-12 pt-2">
								<button
									onclick={toggleMobileMenu}
									aria-label="Close menu"
									class="ml-1 flex h-10 w-10 items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
								>
									<i class="fas fa-times text-white"></i>
								</button>
							</div>
							<div class="h-0 flex-1 overflow-y-auto pb-4 pt-5">
								<div class="flex flex-shrink-0 items-center px-4">
									<i class="fas fa-car-crash mr-2 text-2xl text-white"></i>
									<span class="text-xl font-bold text-white">VBAMS</span>
								</div>
								<nav class="mt-5 space-y-1 px-2">
									<a
										href="/dashboard"
										onclick={toggleMobileMenu}
										class="group flex items-center rounded-md px-2 py-2 text-base font-medium text-blue-100 {currentTheme.navItemHover}"
									>
										<i class="fas fa-tachometer-alt mr-4"></i>
										Dashboard
									</a>
									<a
										href="/vehicles"
										onclick={toggleMobileMenu}
										class="group flex items-center rounded-md px-2 py-2 text-base font-medium text-blue-100 {currentTheme.navItemHover}"
									>
										<i class="fas fa-car mr-4"></i>
										My Vehicles
									</a>
									<a
										href="/breakdowns"
										onclick={toggleMobileMenu}
										class="group flex items-center rounded-md px-2 py-2 text-base font-medium text-blue-100 {currentTheme.navItemHover}"
									>
										<i class="fas fa-exclamation-triangle mr-4"></i>
										Breakdowns
									</a>
									<a
										href="/assistance"
										onclick={toggleMobileMenu}
										class="group flex items-center rounded-md px-2 py-2 text-base font-medium text-blue-100 {currentTheme.navItemHover}"
									>
										<i class="fas fa-handshake mr-4"></i>
										Assistance
									</a>
									<a
										href="/profile"
										onclick={toggleMobileMenu}
										class="group flex items-center rounded-md px-2 py-2 text-base font-medium text-blue-100 {currentTheme.navItemHover}"
									>
										<i class="fas fa-user mr-4"></i>
										Profile
									</a>
								</nav>
							</div>
						</div>
					</div>
				</div>
			{/if}

			<!-- Main content -->
			<div class="flex w-0 flex-1 flex-col overflow-hidden">
				<!-- Top navigation -->
				<div class="relative z-10 flex h-16 flex-shrink-0 bg-white shadow">
					<button
						onclick={toggleMobileMenu}
						aria-label="Open menu"
						class="border-r border-gray-200 px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 md:hidden"
					>
						<i class="fas fa-bars"></i>
					</button>
					<div class="flex flex-1 justify-between px-4">
						<div class="flex flex-1 items-center">
							<div class="flex items-center text-lg font-bold text-gray-700">
								<i
									class="fas fa-car-crash mr-2 text-2xl"
									class:text-orange-600={$user?.role === 'admin'}
									class:text-green-600={$user?.role === 'service_provider'}
									class:text-blue-600={$user?.role === 'driver'}
								></i>
								<span class="mr-2">VBAMS</span>
								<span
									class="rounded-full px-2 py-0.5 text-xs font-semibold uppercase tracking-wide"
									class:bg-orange-100={$user?.role === 'admin'}
									class:text-orange-800={$user?.role === 'admin'}
									class:bg-green-100={$user?.role === 'service_provider'}
									class:text-green-800={$user?.role === 'service_provider'}
									class:bg-blue-100={$user?.role === 'driver'}
									class:text-blue-800={$user?.role === 'driver'}
								>
									{$user?.role?.replace('_', ' ')}
								</span>
							</div>
						</div>
						<div class="ml-4 flex items-center md:ml-6">
							{#if $user?.role === 'driver'}
								<a
									href="/assistance"
									class="flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
								>
									<i class="fas fa-plus mr-2"></i>
									Report Breakdown
								</a>
							{/if}
						</div>
					</div>
				</div>

				<!-- Page content -->
				<main class="relative flex-1 overflow-y-auto focus:outline-none">
					<div class="py-6">
						<div class="mx-auto max-w-7xl px-4 sm:px-6 md:px-8">
							{@render children()}
						</div>
					</div>
				</main>
			</div>
		</div>
	{:else}
		<!-- Public Layout (no mock app link) -->
		<div class="mx-auto max-w-7xl p-6">
			{@render children()}
		</div>
	{/if}
</div>
