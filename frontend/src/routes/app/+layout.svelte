<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { logout, user } from '$lib/stores/auth';
	import { page } from '$app/stores';
	let mobileOpen = false;

	function toggleMobile() {
		mobileOpen = !mobileOpen;
	}

	function handleLogout() {
		logout();
		goto('/');
	}
</script>

<svelte:head>
	<title>VBAMS App</title>
</svelte:head>

<div class="flex min-h-screen bg-white text-gray-800">
	<!-- Sidebar -->
	<aside class="hidden md:flex md:flex-shrink-0">
		<div class="flex w-72 flex-col border-r bg-white shadow-lg">
			<div class="flex h-16 items-center border-b px-6">
				<div class="flex items-center gap-3">
					<div
						class="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 text-white"
					>
						<i class="fas fa-car-crash"></i>
					</div>
					<div>
						<div class="text-lg font-bold">VBAMS</div>
						<div class="text-xs text-gray-500">Vehicle Assistance</div>
					</div>
				</div>
			</div>
			<nav class="flex-1 space-y-1 px-4 py-6">
				<a
					href="/app/dashboard"
					class="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-gray-50 {$page
						.url.pathname === '/app/dashboard'
						? 'bg-gray-50 shadow-sm'
						: ''}"
				>
					<i class="fas fa-tachometer-alt w-5 text-gray-600"></i>
					<span>Dashboard</span>
				</a>
				<a
					href="/app/vehicles"
					class="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-gray-50 {$page.url.pathname.startsWith(
						'/app/vehicles'
					)
						? 'bg-gray-50 shadow-sm'
						: ''}"
				>
					<i class="fas fa-car w-5 text-gray-600"></i>
					<span>Vehicles</span>
				</a>
				<a
					href="/app/breakdowns"
					class="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-gray-50 {$page.url.pathname.startsWith(
						'/app/breakdowns'
					)
						? 'bg-gray-50 shadow-sm'
						: ''}"
				>
					<i class="fas fa-exclamation-triangle w-5 text-gray-600"></i>
					<span>Breakdowns</span>
				</a>
				<a
					href="/app/assistance"
					class="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-gray-50 {$page.url.pathname.startsWith(
						'/app/assistance'
					)
						? 'bg-gray-50 shadow-sm'
						: ''}"
				>
					<i class="fas fa-hands-helping w-5 text-gray-600"></i>
					<span>Assistance</span>
				</a>
				<a
					href="/app/profile"
					class="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-gray-50 {$page.url.pathname.startsWith(
						'/app/profile'
					)
						? 'bg-gray-50 shadow-sm'
						: ''}"
				>
					<i class="fas fa-user w-5 text-gray-600"></i>
					<span>Profile</span>
				</a>
			</nav>
			<div class="border-t p-4">
				<button onclick={handleLogout} class="w-full text-left text-sm text-red-600"
					>Sign out</button
				>
			</div>
		</div>
	</aside>

	<!-- Mobile sidebar -->
	{#if mobileOpen}
		<div class="fixed inset-0 z-40 flex md:hidden">
			<div
				class="fixed inset-0 bg-black opacity-30"
				onclick={toggleMobile}
				aria-hidden="true"
			></div>
			<div class="relative flex w-full max-w-xs flex-1 flex-col bg-white shadow-lg">
				<div class="flex h-16 items-center border-b px-4">
					<div class="flex items-center gap-3">
						<div
							class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white"
						>
							<i class="fas fa-car-crash"></i>
						</div>
						<div class="font-bold">VBAMS</div>
					</div>
				</div>
				<nav class="space-y-1 px-2 py-4">
					<a
						href="/app/dashboard"
						onclick={toggleMobile}
						class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
						>Dashboard</a
					>
					<a
						href="/app/vehicles"
						onclick={toggleMobile}
						class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
						>Vehicles</a
					>
					<a
						href="/app/breakdowns"
						onclick={toggleMobile}
						class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
						>Breakdowns</a
					>
					<a
						href="/app/assistance"
						onclick={toggleMobile}
						class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
						>Assistance</a
					>
					<a
						href="/app/profile"
						onclick={toggleMobile}
						class="block rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
						>Profile</a
					>
				</nav>
				<div class="border-t p-4">
					<button
						onclick={() => {
							toggleMobile();
							handleLogout();
						}}
						class="w-full text-left text-sm text-red-600">Sign out</button
					>
				</div>
			</div>
		</div>
	{/if}

	<!-- Main content -->
	<div class="flex flex-1 flex-col">
		<!-- Topbar -->
		<header class="sticky top-0 z-10 flex h-16 items-center justify-between border-b bg-white px-6">
			<div class="flex items-center gap-4">
				<button
					class="rounded-md p-2 hover:bg-gray-100 md:hidden"
					onclick={toggleMobile}
					aria-label="Open sidebar"
				>
					<i class="fas fa-bars text-gray-700"></i>
				</button>
				<div>
					<h2 class="text-lg font-semibold">App</h2>
					<div class="text-xs text-gray-500">Vehicle Breakdown Assistance</div>
				</div>
			</div>

			<div class="flex items-center gap-4">
				<div class="relative hidden sm:block">
					<input
						placeholder="Search..."
						class="rounded-md border bg-gray-50 py-2 pl-3 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
					/>
					<div class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400">
						<i class="fas fa-search"></i>
					</div>
				</div>

				<button class="rounded-full p-2 hover:bg-gray-100">
					<i class="fas fa-bell text-gray-600"></i>
				</button>

				<div class="flex items-center gap-3">
					<div
						class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-gray-700"
					>
						{#if $user}{$user.first_name ? $user.first_name[0] : 'U'}{/if}
					</div>
					<div class="hidden text-sm text-gray-700 sm:block">
						{#if $user}{$user.first_name} {$user.last_name}{/if}
					</div>
				</div>
			</div>
		</header>

		<main class="overflow-auto p-6">
			<div class="mx-auto max-w-7xl">
				<div class="rounded-lg bg-white p-6 shadow-sm">
					<slot />
				</div>
			</div>
		</main>
	</div>
</div>
