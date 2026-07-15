<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const API_URL = `${API_BASE_URL}/api/posts`

const DEFAULT_IMAGE =
  'https://images.unsplash.com/photo-1507525428034-b723cf961d3e' +
  '?auto=format&fit=crop&w=1000&q=80'

const posts = ref([])
const selectedPost = ref(null)

const isLoading = ref(true)
const errorMessage = ref('')

const heightClasses = ['h-56', 'h-72', 'h-64', 'h-80', 'h-60']

async function loadPosts() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await axios.get(API_URL)

    console.log('게시글 응답:', response.data)

    posts.value = Array.isArray(response.data)
      ? response.data
      : response.data.items || []
  } catch (error) {
    console.error('게시글 로드 실패:', error)
    console.error('백엔드 응답:', error.response?.data)

    errorMessage.value =
      '게시글을 불러오지 못했습니다. FastAPI 서버가 실행 중인지 확인해 주세요.'
  } finally {
    isLoading.value = false
  }
}

function goToEditPage(postId) {
  closeModal()
  router.push(`/board/edit/${postId}`)
}

function openModal(post) {
  selectedPost.value = post
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  selectedPost.value = null
  document.body.style.overflow = ''
}

function goToWritePage() {
  router.push('/board/write')
}

function formatDate(dateString) {
  if (!dateString) {
    return ''
  }

  const date = new Date(dateString)

  if (Number.isNaN(date.getTime())) {
    return ''
  }

  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function handleImageError(event) {
  event.target.onerror = null
  event.target.src = DEFAULT_IMAGE
}

function handleKeydown(event) {
  if (event.key === 'Escape' && selectedPost.value) {
    closeModal()
  }
}

onMounted(() => {
  loadPosts()
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 p-6 text-slate-800 md:p-10">
    <!-- 상단 메뉴 -->
    <header class="mx-auto mb-10 flex w-full max-w-7xl justify-center">
      <nav
        class="flex gap-1 rounded-full border border-slate-200 bg-white/80 px-2 py-1.5 shadow-sm backdrop-blur-md"
      >
        <RouterLink
          to="/"
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
        >
          홈
        </RouterLink>

        <RouterLink
          to="/board"
          class="rounded-full bg-slate-900 px-6 py-2 text-sm font-semibold text-white shadow-sm"
        >
          게시판
        </RouterLink>

        <RouterLink
          to="/map"
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
        >
          지도
        </RouterLink>
      </nav>
    </header>

    <!-- 게시판 본문 -->
    <main class="mx-auto w-full max-w-7xl">
      <div class="mb-8 flex items-center justify-between px-2">
        <h1 class="text-3xl font-extrabold text-slate-900">
          <i class="fa-solid fa-camera-retro mr-2 text-sky-500"></i>
          여행 추천 게시판
        </h1>

        <button
          type="button"
          class="rounded-full bg-sky-500 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-600"
          @click="goToWritePage"
        >
          <i class="fa-solid fa-pen mr-1"></i>
          글쓰기
        </button>
      </div>

      <!-- 로딩 상태 -->
      <div
        v-if="isLoading"
        class="py-20 text-center text-slate-400"
      >
        <i class="fa-solid fa-spinner fa-spin mb-2 text-3xl"></i>
        <p>게시글을 불러오는 중...</p>
      </div>

      <!-- 오류 상태 -->
      <div
        v-else-if="errorMessage"
        class="py-20 text-center font-semibold text-rose-500"
      >
        <i class="fa-solid fa-circle-exclamation mb-2 text-3xl"></i>

        <p>게시글을 불러오지 못했습니다.</p>

        <p class="mt-2 text-sm font-normal text-slate-400">
          FastAPI 서버가 실행 중인지 확인해 주세요.
        </p>

        <button
          type="button"
          class="mt-5 rounded-xl bg-slate-900 px-5 py-2 text-sm text-white transition hover:bg-slate-700"
          @click="loadPosts"
        >
          다시 불러오기
        </button>
      </div>

      <!-- 빈 게시판 -->
      <div
        v-else-if="posts.length === 0"
        class="py-20 text-center text-slate-400"
      >
        <i class="fa-regular fa-folder-open mb-3 text-3xl"></i>
        <p>등록된 게시글이 없습니다.</p>
      </div>

      <!-- 게시글 목록 -->
      <div
        v-else
        class="w-full columns-1 gap-6 sm:columns-2 md:columns-3 lg:columns-4"
      >
        <article
          v-for="(post, index) in posts"
          :key="post.id ?? index"
          :class="[
            'masonry-item group relative w-full cursor-pointer overflow-hidden rounded-2xl border border-slate-200 bg-slate-200 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl',
            heightClasses[index % heightClasses.length],
          ]"
          tabindex="0"
          @click="openModal(post)"
          @keydown.enter="openModal(post)"
        >
          <img
            :src="post.image_url || DEFAULT_IMAGE"
            :alt="post.title || '게시글 이미지'"
            class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            @error="handleImageError"
          />

          <div
            class="absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/85 via-black/25 to-transparent p-4"
          >
            <span class="mb-1 text-xs font-semibold text-sky-300">
              {{ post.category || '광주·전라권' }}
            </span>

            <h2 class="line-clamp-2 text-base font-bold text-white md:text-lg">
              {{ post.title || '제목 없음' }}
            </h2>

            <p class="mt-1 line-clamp-2 text-xs text-slate-300">
              {{ post.content || '내용이 없습니다.' }}
            </p>

            <p class="mt-3 text-xs text-slate-400">
              {{ formatDate(post.created_at) }}
            </p>
          </div>
        </article>
      </div>
    </main>

    <!-- 상세보기 모달 -->
    <div
      v-if="selectedPost"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-label="게시글 상세보기"
      @click.self="closeModal"
    >
      <div
        class="flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-2xl"
      >
        <!-- 게시글 이미지 -->
        <div class="relative h-64 w-full flex-shrink-0 bg-slate-200 sm:h-80">
          <img
            :src="selectedPost.image_url || DEFAULT_IMAGE"
            :alt="selectedPost.title || '게시글 이미지'"
            class="h-full w-full object-cover"
            @error="handleImageError"
          />

          <button
            type="button"
            class="absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full bg-black/50 text-white transition hover:bg-black/70"
            aria-label="상세보기 닫기"
            @click="closeModal"
          >
            <i class="fa-solid fa-xmark text-lg"></i>
          </button>
        </div>

        <!-- 게시글 내용 -->
        <div class="space-y-4 overflow-y-auto p-6">
          <div>
            <span
              class="text-xs font-semibold uppercase tracking-wider text-sky-600"
            >
              {{ selectedPost.category || '광주·전라권' }}
            </span>

            <h2 class="mt-1 text-2xl font-bold text-slate-900">
              {{ selectedPost.title || '제목 없음' }}
            </h2>

            <p class="mt-2 text-xs text-slate-400">
              {{ formatDate(selectedPost.created_at) }}
            </p>
          </div>

          <p
            class="whitespace-pre-line text-sm leading-relaxed text-slate-600 md:text-base"
          >
            {{ selectedPost.content || '내용이 없습니다.' }}
          </p>

          <!-- 추후 수정·삭제 기능을 연결할 영역 -->
          <div class="flex justify-end gap-2 border-t border-slate-100 pt-4">
          <button
            type="button"
            class="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
            @click="goToEditPage(selectedPost.id)"
          >
            수정
          </button>

            <button
              type="button"
              class="rounded-lg bg-rose-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-rose-600"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.masonry-item {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}
</style>