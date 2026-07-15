<script setup>
import { ref } from 'vue'

const chatMessage = ref('')

function submitChat() {
  const message = chatMessage.value.trim()

  if (!message) {
    return
  }

  console.log('챗봇 질문:', message)

  // 추후 FastAPI POST /api/chat 요청을 이곳에 구현
  chatMessage.value = ''
}
</script>

<template>
  <div
    class="bg-slate-50 text-slate-800 antialiased overflow-hidden h-screen flex flex-col justify-between p-6 md:p-10"
  >
    <!-- 상단 내비게이션 -->
    <header class="w-full max-w-7xl mx-auto flex justify-center">
      <nav
        class="bg-white/80 backdrop-blur-md border border-slate-200 shadow-sm px-2 py-1.5 rounded-full flex gap-1"
      >
        <RouterLink
          to="/"
          class="px-6 py-2 rounded-full font-semibold text-sm transition-all duration-200 bg-slate-900 text-white shadow-sm"
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

    <!-- 메인 콘텐츠 -->
    <main
      class="w-full max-w-7xl mx-auto flex-1 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center my-6 min-h-0"
    >
      <!-- 좌측 콘텐츠 -->
      <section
        class="lg:col-span-5 flex flex-col justify-center items-start space-y-6"
      >
        <div class="space-y-2">
          <span
            class="text-sky-600 font-bold tracking-wider text-sm uppercase"
          >
            Travel Recommendation
          </span>

          <h1
            class="text-4xl md:text-5xl font-extrabold leading-tight tracking-tight text-slate-900"
          >
            당신의 취향이<br />

            <span
              class="text-transparent bg-clip-text bg-gradient-to-r from-sky-500 to-indigo-600"
            >
              목적지가 되는 순간
            </span>
          </h1>

          <p class="text-slate-500 text-base mt-2">
            복잡한 계획은 그만. 몇 가지 질문으로 당신에게 딱 맞는 숨은
            여행지를 찾아드려요.
          </p>
        </div>

        <!-- 여행 성향 테스트 -->
        <RouterLink
          to="/favorite"
          class="group inline-flex bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-bold px-8 py-4 rounded-2xl shadow-lg shadow-sky-500/20 hover:shadow-xl hover:shadow-sky-500/30 hover:-translate-y-0.5 transition-all duration-200 items-center gap-3 text-base"
        >
          <span>내 여행 성향 테스트하기</span>

          <i
            class="fa-solid fa-arrow-right group-hover:translate-x-1 transition-transform"
          ></i>
        </RouterLink>
      </section>

      <!-- 우측 이미지 영역 -->
      <section
        class="lg:col-span-7 h-full w-full min-h-[300px] lg:min-h-0 rounded-3xl overflow-hidden shadow-xl border border-slate-200/60 relative group"
      >
        <img
          src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
          alt="아름다운 해변 여행지 배경"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
        />

        <div
          class="absolute inset-0 bg-gradient-to-t from-slate-950/40 via-transparent to-transparent"
        ></div>

        <div
          class="absolute bottom-6 right-6 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-xl text-xs font-semibold shadow-sm text-slate-700"
        >
          <i class="fa-solid fa-location-dot text-rose-500 mr-1"></i>
          지금 떠나기 좋은 추천 휴양지
        </div>
      </section>
    </main>

    <!-- 챗봇 입력창 -->
    <footer class="w-full max-w-5xl mx-auto">
      <form
        class="bg-white border border-slate-200 shadow-xl rounded-2xl p-2.5 flex items-center gap-3 focus-within:border-sky-500 focus-within:ring-2 focus-within:ring-sky-100 transition-all duration-200"
        @submit.prevent="submitChat"
      >
        <div
          class="w-10 h-10 bg-sky-50 rounded-xl flex items-center justify-center text-sky-500 flex-shrink-0"
        >
          <i class="fa-solid fa-robot text-lg"></i>
        </div>

        <input
          v-model="chatMessage"
          type="text"
          placeholder="어디로 떠나고 싶으신가요? (예: '5월에 가기 좋은 조용한 바다 추천해줘')"
          class="w-full bg-transparent text-sm md:text-base text-slate-800 placeholder-slate-400 focus:outline-none px-1"
        />

        <button
          type="submit"
          class="bg-slate-900 text-white w-10 h-10 rounded-xl flex items-center justify-center hover:bg-slate-800 transition-colors flex-shrink-0"
          aria-label="질문 전송"
        >
          <i class="fa-solid fa-paper-plane text-sm"></i>
        </button>
      </form>
    </footer>
  </div>
</template>

<style scoped>
:global(body) {
  margin: 0;
  min-width: 320px;
  font-family: 'Pretendard', sans-serif;
}
</style>