<script setup>
import ChatBot from '../components/ChatBot.vue'
</script>

<template>
  <div class="min-h-screen bg-slate-50 p-6 text-slate-800 md:p-10">
    <header class="mx-auto mb-6 flex w-full max-w-7xl justify-center">
      <nav class="flex gap-1 rounded-full border border-slate-200 bg-white/80 px-2 py-1.5 shadow-sm backdrop-blur-md">
        <RouterLink to="/" class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100">홈</RouterLink>
        <RouterLink to="/chat" class="rounded-full bg-slate-900 px-6 py-2 text-sm font-semibold text-white shadow-sm">챗봇</RouterLink>
      </nav>
    </header>

    <main class="mx-auto w-full max-w-3xl">
      <ChatBot />
    </main>
  </div>
</template>

<style scoped>
.rounded-xl { border-radius: 12px; }
</style>
