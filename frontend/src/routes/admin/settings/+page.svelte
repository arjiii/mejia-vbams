<script lang="ts">
	let systemSettings = $state({
		siteName: 'VBAMS',
		contactEmail: 'admin@vbams.com',
		maxDistance: 50,
		autoApproveProviders: false,
		maintenanceMode: false
	});

	function saveSettings() {
		console.log('Saving settings:', systemSettings);
		// Save settings logic
	}
</script>

<svelte:head>
	<title>Settings - VBAMS</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold text-gray-900">System Settings</h1>
		<p class="mt-2 text-sm text-gray-600">Configure system-wide settings and preferences</p>
	</div>

	<!-- General Settings -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<h2 class="mb-6 text-xl font-bold text-gray-900">General Settings</h2>
		<div class="space-y-4">
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Site Name</label>
				<input
					type="text"
					bind:value={systemSettings.siteName}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-200"
				/>
			</div>
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">Contact Email</label>
				<input
					type="email"
					bind:value={systemSettings.contactEmail}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-200"
				/>
			</div>
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700"
					>Maximum Service Distance (km)</label
				>
				<input
					type="number"
					bind:value={systemSettings.maxDistance}
					class="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-200"
				/>
			</div>
		</div>
	</div>

	<!-- Provider Settings -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<h2 class="mb-6 text-xl font-bold text-gray-900">Provider Management</h2>
		<div class="space-y-4">
			<div class="flex items-center justify-between rounded-lg border border-gray-200 p-4">
				<div>
					<h3 class="font-medium text-gray-900">Auto-Approve Providers</h3>
					<p class="text-sm text-gray-500">
						Automatically verify new service provider registrations
					</p>
				</div>
				<button
					onclick={() =>
						(systemSettings.autoApproveProviders = !systemSettings.autoApproveProviders)}
					class={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out ${systemSettings.autoApproveProviders ? 'bg-green-600' : 'bg-gray-300'}`}
				>
					<span
						class={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${systemSettings.autoApproveProviders ? 'translate-x-5' : 'translate-x-0'}`}
					></span>
				</button>
			</div>
		</div>
	</div>

	<!-- System Maintenance -->
	<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-lg">
		<h2 class="mb-6 text-xl font-bold text-gray-900">System Maintenance</h2>
		<div class="space-y-4">
			<div
				class="flex items-center justify-between rounded-lg border border-yellow-200 bg-yellow-50 p-4"
			>
				<div>
					<h3 class="font-medium text-yellow-900">Maintenance Mode</h3>
					<p class="text-sm text-yellow-700">Disable public access for system maintenance</p>
				</div>
				<button
					onclick={() => (systemSettings.maintenanceMode = !systemSettings.maintenanceMode)}
					class={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out ${systemSettings.maintenanceMode ? 'bg-red-600' : 'bg-gray-300'}`}
				>
					<span
						class={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${systemSettings.maintenanceMode ? 'translate-x-5' : 'translate-x-0'}`}
					></span>
				</button>
			</div>
		</div>
	</div>

	<!-- Save Button -->
	<div class="flex justify-end">
		<button
			onclick={saveSettings}
			class="rounded-lg bg-gradient-to-r from-red-600 to-orange-600 px-6 py-3 text-sm font-bold text-white shadow-lg transition-all hover:from-red-700 hover:to-orange-700"
		>
			<i class="fas fa-save mr-2"></i>
			Save Settings
		</button>
	</div>
</div>
