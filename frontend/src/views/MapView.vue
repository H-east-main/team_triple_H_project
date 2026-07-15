<template>
  <div
    class="min-h-screen bg-slate-50 p-6 text-slate-800 antialiased md:p-10"
  >
    <!-- 상단 내비게이션 -->
    <header class="mx-auto flex w-full max-w-7xl justify-center">
      <nav
        class="flex gap-1 rounded-full border border-slate-200 bg-white/80 px-2 py-1.5 shadow-sm backdrop-blur-md"
      >
        <RouterLink
          to="/"
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition-all duration-200 hover:bg-slate-100"
        >
          <i class="fa-solid fa-star mr-2"></i>
          추천
        </RouterLink>

        <RouterLink
          to="/board"
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition-all duration-200 hover:bg-slate-100"
        >
          <i class="fa-regular fa-clipboard mr-2"></i>
          게시판
        </RouterLink>

        <RouterLink
          to="/map"
          class="rounded-full bg-slate-900 px-6 py-2 text-sm font-semibold text-white shadow-sm transition-all duration-200"
        >
          <i class="fa-solid fa-map-location-dot mr-2"></i>
          지도
        </RouterLink>
      </nav>
    </header>

    <!-- 지도 콘텐츠 -->
    <main class="mx-auto mt-12 w-full max-w-4xl">
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-slate-900">
          <i class="fa-solid fa-map-location-dot mr-2 text-sky-500"></i>
          지역 정보 지도
        </h1>

        <p class="mt-4 text-slate-500">
          관광지와 맛집 등 지역 정보를 지도에서 확인할 수 있습니다.
        </p>
      </div>

      <!-- 실제 지도 라이브러리가 표시될 영역 -->
      <section
        class="flex min-h-[500px] items-center justify-center rounded-3xl border border-slate-200 bg-white shadow-sm"
      >
        <div class="text-center text-slate-400">
          <i class="fa-regular fa-map mb-4 text-5xl"></i>

          <p class="font-semibold">지도 준비 중</p>

          <p class="mt-2 text-sm">
            Leaflet 또는 Kakao Maps를 이 영역에 적용할 예정입니다.
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
:global(body) {
  margin: 0;
  min-width: 320px;
  font-family: 'Pretendard', sans-serif;
}
</style>