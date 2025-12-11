<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { isAuthenticated, user } from '$lib/stores/auth';
	import DriverDashboard from '$lib/components/dashboard/DriverDashboard.svelte';
	import ServiceProviderDashboard from '$lib/components/dashboard/ServiceProviderDashboard.svelte';
	import AdminDashboard from '$lib/components/dashboard/AdminDashboard.svelte';

	let userRole = $state('driver');

	// Check authentication only on client side
	onMount(() => {
		if (!$isAuthenticated) {
			goto('/login');
		}
	});

	$effect(() => {
		if ($user) {
			userRole = $user.role;
		}
	});
</script>

<svelte:head>
	<title>Dashboard - VBAMS</title>
</svelte:head>

{#if $user}
	{#if userRole === 'admin'}
		<AdminDashboard />
	{:else if userRole === 'service_provider'}
		<ServiceProviderDashboard />
	{:else}
		<DriverDashboard />
	{/if}
{:else}
	<div class="flex h-64 items-center justify-center">
		<div class="h-32 w-32 animate-spin rounded-full border-b-2 border-blue-600"></div>
	</div>
{/if}
