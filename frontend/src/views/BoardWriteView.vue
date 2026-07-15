<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const API_URL = `${API_BASE_URL}/api/posts`

const category = ref('광주·전라권')
const title = ref('')
const content = ref('')
const password = ref('')
const imageUrl = ref('')

const isSubmitting = ref(false)
const errorMessage = ref('')

const categories = [
  '광주·전라권',
  '여행후기',
  '맛집',
  '관광지',
  '축제',
  '여행코스',
]

const isFormValid = computed(() => {
  return (
    category.value.trim() &&
    title.value.trim() &&
    content.value.trim() &&
    password.value.trim()
  )
})

function goBack() {
  router.push('/board')
}

async function submitPost() {
  if (!isFormValid.value) {
    errorMessage.value =
      '카테고리, 제목, 내용, 수정·삭제용 비밀번호를 모두 입력해 주세요.'
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  const requestBody = {
    category: category.value.trim(),
    title: title.value.trim(),
    content: content.value.trim(),
    password: password.value.trim(),
    image_url: imageUrl.value.trim() || null,
  }

  try {
    await axios.post(API_URL, requestBody)
    alert('게시글이 등록되었습니다.')
    await router.push('/board')
  } catch (error) {
    console.error('게시글 등록 실패:', error)
    console.error('백엔드 응답:', error.response?.data)

    const detail = error.response?.data?.detail

    if (Array.isArray(detail)) {
      errorMessage.value =
        detail.map((item) => item.msg).join(', ') ||
        '입력값을 다시 확인해 주세요.'
    } else {
      errorMessage.value =
        detail ||
        '게시글 등록에 실패했습니다. FastAPI 서버와 요청 주소를 확인해 주세요.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 p-6 text-slate-800 md:p-10">
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

    <main class="mx-auto w-full max-w-5xl">
      <div class="mb-8 flex items-center justify-between">
        <div>
          <p class="mb-2 text-sm font-bold text-sky-500">
            <i class="fa-solid fa-pen-to-square mr-2"></i>
            여행 경험 공유
          </p>

          <h1 class="text-3xl font-extrabold text-slate-900 md:text-4xl">
            여행 추천 글쓰기
          </h1>

          <p class="mt-3 text-sm text-slate-500 md:text-base">
            직접 다녀온 장소와 여행 팁을 다른 사용자들과 공유해 보세요.
          </p>
        </div>

        <button
          type="button"
          class="hidden rounded-full border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:bg-slate-100 sm:block"
          @click="goBack"
        >
          <i class="fa-solid fa-arrow-left mr-2"></i>
          게시판으로
        </button>
      </div>

      <form
        class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm"
        @submit.prevent="submitPost"
      >
        <div class="grid grid-cols-1 lg:grid-cols-[1.15fr_0.85fr]">
          <section class="space-y-6 p-6 md:p-8 lg:border-r lg:border-slate-100">
            <div>
              <label
                for="category"
                class="mb-2 block text-sm font-bold text-slate-700"
              >
                카테고리
              </label>

              <select
                id="category"
                v-model="category"
                class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              >
                <option
                  v-for="item in categories"
                  :key="item"
                  :value="item"
                >
                  {{ item }}
                </option>
              </select>
            </div>

            <div>
              <div class="mb-2 flex items-center justify-between">
                <label
                  for="title"
                  class="text-sm font-bold text-slate-700"
                >
                  제목
                </label>

                <span class="text-xs text-slate-400">
                  {{ title.length }}/100
                </span>
              </div>

              <input
                id="title"
                v-model="title"
                type="text"
                maxlength="100"
                placeholder="예: 담양 메타세쿼이아길 힐링 코스"
                class="w-full rounded-2xl border border-slate-200 px-4 py-3.5 text-sm outline-none transition placeholder:text-slate-300 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              />
            </div>

            <div>
              <div class="mb-2 flex items-center justify-between">
                <label
                  for="content"
                  class="text-sm font-bold text-slate-700"
                >
                  내용
                </label>

                <span class="text-xs text-slate-400">
                  {{ content.length }}/3000
                </span>
              </div>

              <textarea
                id="content"
                v-model="content"
                rows="12"
                maxlength="3000"
                placeholder="장소의 분위기, 추천 이유, 방문 팁 등을 자유롭게 작성해 주세요."
                class="w-full resize-none rounded-2xl border border-slate-200 px-4 py-4 text-sm leading-7 outline-none transition placeholder:text-slate-300 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              ></textarea>
            </div>

            <div>
              <label
                for="password"
                class="mb-2 block text-sm font-bold text-slate-700"
              >
                수정·삭제용 비밀번호
              </label>

              <input
                id="password"
                v-model="password"
                type="password"
                maxlength="50"
                autocomplete="new-password"
                placeholder="나중에 수정하거나 삭제할 때 사용합니다"
                class="w-full rounded-2xl border border-slate-200 px-4 py-3.5 text-sm outline-none transition placeholder:text-slate-300 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              />

              <p class="mt-2 text-xs leading-5 text-slate-400">
                익명 게시판이므로 비밀번호를 잊으면 수정과 삭제가 어렵습니다.
              </p>
            </div>
          </section>

          <aside class="bg-slate-50/70 p-6 md:p-8">
            <div class="mb-4">
              <h2 class="text-lg font-extrabold text-slate-900">
                대표 이미지
              </h2>

              <p class="mt-1 text-sm text-slate-500">
                이미지 URL을 입력하면 게시판 카드에 표시됩니다.
              </p>
            </div>

            <div
              class="relative overflow-hidden rounded-3xl border border-dashed border-slate-300 bg-white"
            >
              <img
                v-if="imageUrl"
                :src="imageUrl"
                alt="게시글 이미지 미리보기"
                class="h-80 w-full object-cover"
              />

              <div
                v-else
                class="flex h-80 flex-col items-center justify-center px-8 text-center text-slate-400"
              >
                <div
                  class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-sky-50 text-sky-400"
                >
                  <i class="fa-regular fa-image text-2xl"></i>
                </div>

                <p class="text-sm font-bold text-slate-600">
                  이미지 미리보기
                </p>

                <p class="mt-2 text-xs leading-5">
                  아래 입력창에 이미지 주소를 넣으면 여기에 바로 표시됩니다.
                </p>
              </div>
            </div>

            <div class="mt-5">
              <label
                for="imageUrl"
                class="mb-2 block text-sm font-bold text-slate-700"
              >
                이미지 URL
              </label>

              <input
                id="imageUrl"
                v-model="imageUrl"
                type="url"
                placeholder="https://example.com/image.jpg"
                class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3.5 text-sm outline-none transition placeholder:text-slate-300 focus:border-sky-400 focus:ring-4 focus:ring-sky-100"
              />

              <p class="mt-2 text-xs leading-5 text-slate-400">
                입력하지 않으면 게시판 목록에서 기본 이미지가 표시됩니다.
              </p>
            </div>
          </aside>
        </div>

        <div
          v-if="errorMessage"
          class="mx-6 mb-2 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-600 md:mx-8"
        >
          <i class="fa-solid fa-circle-exclamation mr-2"></i>
          {{ errorMessage }}
        </div>

        <div
          class="flex flex-col-reverse gap-3 border-t border-slate-100 bg-white px-6 py-5 sm:flex-row sm:justify-end md:px-8"
        >
          <button
            type="button"
            class="rounded-full border border-slate-200 px-6 py-3 text-sm font-bold text-slate-600 transition hover:bg-slate-100"
            :disabled="isSubmitting"
            @click="goBack"
          >
            취소
          </button>

          <button
            type="submit"
            class="rounded-full bg-sky-500 px-7 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-sky-600 disabled:cursor-not-allowed disabled:bg-slate-300"
            :disabled="isSubmitting || !isFormValid"
          >
            <template v-if="isSubmitting">
              <i class="fa-solid fa-spinner fa-spin mr-2"></i>
              등록 중...
            </template>

            <template v-else>
              <i class="fa-solid fa-check mr-2"></i>
              게시글 등록
            </template>
          </button>
        </div>
      </form>
    </main>
  </div>
</template>
