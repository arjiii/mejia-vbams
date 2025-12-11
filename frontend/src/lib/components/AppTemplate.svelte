<script lang="ts">
  export let title = 'VBAMS — App';
</script>

<div class="min-h-screen bg-gray-50">
  <header class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <i class="fas fa-car-crash text-blue-600 text-2xl"></i>
        <h1 class="text-lg font-semibold">{title}</h1>
      </div>
      <nav class="flex items-center gap-4">
        <a href="/app/dashboard" class="text-sm text-gray-700 hover:underline">Dashboard</a>
        <a href="/app/vehicles" class="text-sm text-gray-700 hover:underline">Vehicles</a>
        <a href="/app/breakdowns" class="text-sm text-gray-700 hover:underline">Breakdowns</a>
        <a href="/app/assistance" class="text-sm text-gray-700 hover:underline">Assistance</a>
        <a href="/app/profile" class="text-sm text-gray-700 hover:underline">Profile</a>
        <a href="/register" class="text-sm text-gray-700 hover:underline">Register</a>
        <a href="/login" class="text-sm text-gray-700 hover:underline">Login</a>
      </nav>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-6">
    <slot />
  </main>
</div>
