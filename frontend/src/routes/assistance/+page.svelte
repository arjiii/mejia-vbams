<script lang="ts">
	let selectedVehicle = $state('');
	let issueType = $state('');
	let location = $state('');
	let description = $state('');
	let isSubmitting = $state(false);

	const vehicles = [
		{ id: 1, label: '2020 Toyota Camry (ABC-1234)' },
		{ id: 2, label: '2019 Honda Civic (XYZ-5678)' }
	];

	const issueTypes = [
		'Flat Tire',
		'Dead Battery',
		'Engine Problem',
		'Out of Fuel',
		'Locked Out',
		'Accident',
		'Other'
	];

	async function handleSubmit() {
		isSubmitting = true;
		// Simulate API call
		setTimeout(() => {
			alert('Assistance request submitted! A service provider will contact you soon.');
			// Reset form
			selectedVehicle = '';
			issueType = '';
			location = '';
			description = '';
			isSubmitting = false;
		}, 1500);
	}

	function getCurrentLocation() {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					location = `${position.coords.latitude}, ${position.coords.longitude}`;
				},
				(error) => {
					alert('Unable to get your location. Please enter manually.');
				}
			);
		}
	}
</script>

<svelte:head>
	<title>Request Assistance - VBAMS</title>
</svelte:head>

<div class="mx-auto max-w-3xl space-y-6">
	<!-- Emergency Header -->
	<div class="rounded-2xl bg-gradient-to-r from-red-600 to-orange-600 p-8 text-white shadow-2xl">
		<div class="flex items-center justify-between">
			<div>
				<h1 class="mb-2 text-4xl font-bold">Emergency Assistance</h1>
				<p class="text-red-100">Get help from nearby service providers</p>
			</div>
			<div class="hidden md:block">
				<i class="fas fa-ambulance text-7xl opacity-30"></i>
			</div>
		</div>

		<!-- Emergency Contact -->
		<div class="mt-6 rounded-xl border border-white/20 bg-white/10 p-4 backdrop-blur-sm">
			<p class="mb-2 text-sm">Emergency Hotline:</p>
			<a href="tel:+15551234567" class="flex items-center text-2xl font-bold hover:underline">
				<i class="fas fa-phone-alt mr-3"></i>
				+1 (555) 123-4567
			</a>
		</div>
	</div>

	<!-- Request Form -->
	<div class="rounded-xl border border-gray-200 bg-white p-8 shadow-lg">
		<h2 class="mb-6 text-2xl font-bold text-gray-900">Submit Assistance Request</h2>

		<form
			onsubmit={(e) => {
				e.preventDefault();
				handleSubmit();
			}}
			class="space-y-6"
		>
			<!-- Vehicle Selection -->
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">
					<i class="fas fa-car mr-2 text-blue-600"></i>
					Select Vehicle *
				</label>
				<select
					bind:value={selectedVehicle}
					required
					class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					<option value="">Choose a vehicle...</option>
					{#each vehicles as vehicle}
						<option value={vehicle.id}>{vehicle.label}</option>
					{/each}
				</select>
			</div>

			<!-- Issue Type -->
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">
					<i class="fas fa-exclamation-triangle mr-2 text-yellow-600"></i>
					Issue Type *
				</label>
				<select
					bind:value={issueType}
					required
					class="w-full rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					<option value="">Select issue type...</option>
					{#each issueTypes as type}
						<option value={type}>{type}</option>
					{/each}
				</select>
			</div>

			<!-- Location -->
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">
					<i class="fas fa-map-marker-alt mr-2 text-red-600"></i>
					Current Location *
				</label>
				<div class="flex gap-2">
					<input
						type="text"
						bind:value={location}
						placeholder="Enter your location or use GPS"
						required
						class="flex-1 rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
					/>
					<button
						type="button"
						onclick={getCurrentLocation}
						class="rounded-xl bg-blue-600 px-4 py-3 text-white transition-colors hover:bg-blue-700"
						title="Use current location"
					>
						<i class="fas fa-crosshairs"></i>
					</button>
				</div>
			</div>

			<!-- Description -->
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700">
					<i class="fas fa-comment-alt mr-2 text-gray-600"></i>
					Additional Details
				</label>
				<textarea
					bind:value={description}
					rows="4"
					placeholder="Describe the problem in detail..."
					class="w-full resize-none rounded-xl border border-gray-300 px-4 py-3 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
				></textarea>
			</div>

			<!-- Submit Button -->
			<button
				type="submit"
				disabled={isSubmitting}
				class="w-full rounded-xl bg-gradient-to-r from-red-600 to-orange-600 py-4 font-bold text-white shadow-lg transition-all hover:from-red-700 hover:to-orange-700 disabled:cursor-not-allowed disabled:opacity-50"
			>
				{#if isSubmitting}
					<i class="fas fa-spinner fa-spin mr-2"></i>
					Requesting Assistance...
				{:else}
					<i class="fas fa-paper-plane mr-2"></i>
					Request Assistance Now
				{/if}
			</button>
		</form>
	</div>

	<!-- What Happens Next -->
	<div class="rounded-xl border border-blue-200 bg-blue-50 p-6">
		<h3 class="mb-4 flex items-center font-bold text-gray-900">
			<i class="fas fa-info-circle mr-2 text-blue-600"></i>
			What Happens Next?
		</h3>
		<ol class="space-y-3">
			<li class="flex items-start">
				<span
					class="mr-3 mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white"
					>1</span
				>
				<span class="text-sm text-gray-700">Your request is sent to nearby service providers</span>
			</li>
			<li class="flex items-start">
				<span
					class="mr-3 mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white"
					>2</span
				>
				<span class="text-sm text-gray-700">A provider accepts your request and contacts you</span>
			</li>
			<li class="flex items-start">
				<span
					class="mr-3 mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white"
					>3</span
				>
				<span class="text-sm text-gray-700">Track the provider's arrival in real-time</span>
			</li>
			<li class="flex items-start">
				<span
					class="mr-3 mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white"
					>4</span
				>
				<span class="text-sm text-gray-700">Receive professional service and pay securely</span>
			</li>
		</ol>
	</div>
</div>
