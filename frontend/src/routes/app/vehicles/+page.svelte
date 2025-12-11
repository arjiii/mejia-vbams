<script lang="ts">
  export let title = 'Vehicles';

  type Vehicle = {
    plate: string;
    model: string;
    year: number;
    mileage: string;
    status: 'Active' | 'Inactive' | 'Needs Service';
  };

  let query = '';

  let vehicles: Vehicle[] = [
    { plate: 'ABC-123', model: 'Toyota Vios', year: 2018, mileage: '45,200 km', status: 'Active' },
    { plate: 'XYZ-789', model: 'Honda Civic', year: 2017, mileage: '128,000 km', status: 'Active' },
    { plate: 'LMN-456', model: 'Nissan Almera', year: 2016, mileage: '200,500 km', status: 'Needs Service' }
  ];

  $: filtered = query
    ? vehicles.filter((v) => [v.plate, v.model, String(v.year), v.mileage, v.status].join(' ').toLowerCase().includes(query.trim().toLowerCase()))
    : vehicles;

  function addVehicle() {
    // placeholder: in a real app this would open a modal or navigate to add form
    alert('Add vehicle (dev): this would open a form in the real app.');
  }

  function viewVehicle(v: Vehicle) {
    // placeholder for navigation
    alert(`Open vehicle ${v.plate} — ${v.model}`);
  }

  function statusClass(s: Vehicle['status']) {
    return s === 'Active' ? 'bg-green-100 text-green-800' : s === 'Needs Service' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800';
  }
</script>

<svelte:head>
  <title>App - Vehicles</title>
</svelte:head>

<div class="p-6">
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-semibold text-gray-900">Vehicles</h2>
        <p class="text-sm text-gray-500 mt-1">List of registered vehicles in the system.</p>
      </div>

      <div class="flex items-center space-x-3 w-full md:w-auto">
        <div class="relative flex-1 md:flex-none">
          <input
            type="search"
            placeholder="Search by plate, model, year..."
            bind:value={query}
            class="w-full md:w-64 pl-10 pr-4 py-2 border rounded-md bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
            <i class="fas fa-search"></i>
          </div>
        </div>

        <button on:click={addVehicle} class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm">
          <i class="fas fa-plus mr-2"></i>
          Add Vehicle
        </button>
      </div>
    </div>

    <div class="mt-6">
      <!-- Mobile: card list -->
      <div class="space-y-4 md:hidden">
        {#each filtered as v}
          <article class="border rounded-lg p-4 bg-white shadow-sm flex justify-between items-start">
            <div>
              <div class="flex items-center space-x-3">
                <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 font-semibold">{v.plate.split('-')[0]}</div>
                <div>
                  <h3 class="text-lg font-medium text-gray-900">{v.model}</h3>
                  <p class="text-sm text-gray-500">{v.plate} • {v.year}</p>
                </div>
              </div>
              <div class="mt-3 text-sm text-gray-600">Mileage: {v.mileage}</div>
            </div>
            <div class="flex flex-col items-end space-y-3">
              <span class={`px-2 py-1 text-xs font-semibold rounded ${statusClass(v.status)}`}>{v.status}</span>
              <button on:click={() => viewVehicle(v)} class="text-sm text-blue-600 hover:underline">View</button>
            </div>
          </article>
        {/each}
      </div>

      <!-- Desktop: table -->
      <div class="hidden md:block">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 mt-2">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Plate</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Model</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Year</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mileage</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-100">
              {#each filtered as v}
                <tr class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{v.plate}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{v.model}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{v.year}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{v.mileage}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span class={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${statusClass(v.status)}`}>{v.status}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button on:click={() => viewVehicle(v)} class="text-blue-600 hover:text-blue-800">View</button>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
