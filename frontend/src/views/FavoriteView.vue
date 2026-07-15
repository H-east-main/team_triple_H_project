<template>
  <div class="bg-slate-50 text-slate-800 antialiased min-h-screen p-6 md:p-10">
    <!-- 상단 내비게이션 -->
    <header class="w-full max-w-7xl mx-auto flex justify-center">
      <nav
        class="bg-white/80 backdrop-blur-md border border-slate-200 shadow-sm px-2 py-1.5 rounded-full flex gap-1"
      >
        <RouterLink
          to="/"
          class="px-6 py-2 rounded-full font-semibold text-sm transition-all duration-200 text-slate-600 hover:bg-slate-100"
        >
          <i class="fa-solid fa-star mr-2"></i>
          추천
        </RouterLink>

        <RouterLink
          to="/board"
          class="px-6 py-2 rounded-full font-semibold text-sm transition-all duration-200 text-slate-600 hover:bg-slate-100"
        >
          <i class="fa-regular fa-clipboard mr-2"></i>
          게시판
        </RouterLink>

        <RouterLink
          to="/map"
          class="px-6 py-2 rounded-full font-semibold text-sm transition-all duration-200 text-slate-600 hover:bg-slate-100"
        >
          <i class="fa-solid fa-map-location-dot mr-2"></i>
          지도
        </RouterLink>
      </nav>
    </header>

    <!-- 여행 성향 테스트 영역 -->
    <main class="max-w-4xl mx-auto mt-12">
      <h1 class="text-2xl font-bold">내 여행 성향 테스트</h1>

      <p class="text-slate-500 mt-4">
        테스트 흐름을 여기에 구현하세요. 예를 들어 질문 폼과 결과 페이지를
        구성할 수 있습니다.
      </p>
    </main>
  </div>
</template>