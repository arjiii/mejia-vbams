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

<div class="min-h-screen flex bg-white text-gray-800">
  <!-- Sidebar -->
  <aside class="hidden md:flex md:flex-shrink-0">
    <div class="flex flex-col w-72 bg-white shadow-lg border-r">
      <div class="h-16 flex items-center px-6 border-b">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-500 to-purple-600 flex items-center justify-center text-white">
            <i class="fas fa-car-crash"></i>
          </div>
          <div>
            <div class="font-bold text-lg">VBAMS</div>
            <div class="text-xs text-gray-500">Vehicle Assistance</div>
          </div>
        </div>
      </div>
      <nav class="flex-1 px-4 py-6 space-y-1">
        <a href="/app/dashboard" class="group flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-50 { $page.url.pathname === '/app/dashboard' ? 'bg-gray-50 shadow-sm' : '' }">
          <i class="fas fa-tachometer-alt text-gray-600 w-5"></i>
          <span>Dashboard</span>
        </a>
        <a href="/app/vehicles" class="group flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-50 { $page.url.pathname.startsWith('/app/vehicles') ? 'bg-gray-50 shadow-sm' : '' }">
          <i class="fas fa-car text-gray-600 w-5"></i>
          <span>Vehicles</span>
        </a>
        <a href="/app/breakdowns" class="group flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-50 { $page.url.pathname.startsWith('/app/breakdowns') ? 'bg-gray-50 shadow-sm' : '' }">
          <i class="fas fa-exclamation-triangle text-gray-600 w-5"></i>
          <span>Breakdowns</span>
        </a>
        <a href="/app/assistance" class="group flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-50 { $page.url.pathname.startsWith('/app/assistance') ? 'bg-gray-50 shadow-sm' : '' }">
          <i class="fas fa-hands-helping text-gray-600 w-5"></i>
          <span>Assistance</span>
        </a>
        <a href="/app/profile" class="group flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-50 { $page.url.pathname.startsWith('/app/profile') ? 'bg-gray-50 shadow-sm' : '' }">
          <i class="fas fa-user text-gray-600 w-5"></i>
          <span>Profile</span>
        </a>
      </nav>
      <div class="p-4 border-t">
        <button on:click={handleLogout} class="w-full text-left text-sm text-red-600">Sign out</button>
      </div>
    </div>
  </aside>

  <!-- Mobile sidebar -->
  {#if mobileOpen}
    <div class="fixed inset-0 z-40 flex md:hidden">
      <div class="fixed inset-0 bg-black opacity-30" on:click={toggleMobile}></div>
      <div class="relative flex-1 flex flex-col max-w-xs w-full bg-white shadow-lg">
        <div class="h-16 flex items-center px-4 border-b">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
              <i class="fas fa-car-crash"></i>
            </div>
            <div class="font-bold">VBAMS</div>
          </div>
        </div>
        <nav class="px-2 py-4 space-y-1">
          <a href="/app/dashboard" on:click={toggleMobile} class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">Dashboard</a>
          <a href="/app/vehicles" on:click={toggleMobile} class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">Vehicles</a>
          <a href="/app/breakdowns" on:click={toggleMobile} class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">Breakdowns</a>
          <a href="/app/assistance" on:click={toggleMobile} class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">Assistance</a>
          <a href="/app/profile" on:click={toggleMobile} class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">Profile</a>
        </nav>
        <div class="p-4 border-t">
          <button on:click={() => { toggleMobile(); handleLogout(); }} class="w-full text-left text-sm text-red-600">Sign out</button>
        </div>
      </div>
    </div>
  {/if}

  <!-- Main content -->
  <div class="flex-1 flex flex-col">
    <!-- Topbar -->
    <header class="flex items-center justify-between h-16 bg-white px-6 border-b sticky top-0 z-10">
      <div class="flex items-center gap-4">
        <button class="md:hidden p-2 rounded-md hover:bg-gray-100" on:click={toggleMobile} aria-label="Open sidebar">
          <i class="fas fa-bars text-gray-700"></i>
        </button>
        <div>
          <h2 class="text-lg font-semibold">App</h2>
          <div class="text-xs text-gray-500">Vehicle Breakdown Assistance</div>
        </div>
      </div>

      <div class="flex items-center gap-4">
        <div class="relative hidden sm:block">
          <input placeholder="Search..." class="pl-3 pr-10 py-2 border rounded-md bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <div class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400"><i class="fas fa-search"></i></div>
        </div>

        <button class="p-2 rounded-full hover:bg-gray-100">
          <i class="fas fa-bell text-gray-600"></i>
        </button>

        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-700">{#if $user}{$user.first_name ? $user.first_name[0] : 'U'}{/if}</div>
          <div class="hidden sm:block text-sm text-gray-700">{#if $user}{$user.first_name} {$user.last_name}{/if}</div>
        </div>
      </div>
    </header>

    <main class="p-6 overflow-auto">
      <div class="max-w-7xl mx-auto">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <slot />
        </div>
      </div>
    </main>
  </div>
</div>
