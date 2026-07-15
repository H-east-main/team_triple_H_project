<script setup>
import { computed, ref } from 'vue'
import axios from 'axios'

const testStarted = ref(false)
const testFinished = ref(false)
const currentQuestionIndex = ref(0)

/*
  answers 배열에는 각 질문에서 선택한 선택지의 index가 저장됨.
  예: [0, 2, 1, 3, 0]
*/
const answers = ref([])
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const isSaving = ref(false)
const saveError = ref('')
const isMoving = ref(false)

const questions = [
  {
    id: 1,
    text: '여행지에 도착했을 때 가장 먼저 하고 싶은 일은?',
    options: [
      {
        text: '탁 트인 자연을 바라보며 천천히 산책한다.',
        type: 'healing',
        score: 2,
        icon: 'fa-solid fa-tree',
      },
      {
        text: '지역을 대표하는 박물관이나 문화시설을 방문한다.',
        type: 'culture',
        score: 2,
        icon: 'fa-solid fa-landmark',
      },
      {
        text: '등산, 자전거, 수상 활동처럼 몸을 움직인다.',
        type: 'adventure',
        score: 2,
        icon: 'fa-solid fa-person-hiking',
      },
      {
        text: '골목과 전통시장을 돌아다니며 지역 분위기를 느낀다.',
        type: 'local',
        score: 2,
        icon: 'fa-solid fa-store',
      },
    ],
  },
  {
    id: 2,
    text: '가장 마음에 드는 하루 여행 일정은?',
    options: [
      {
        text: '숲길을 걷고 전망 좋은 곳에서 여유롭게 쉬는 일정',
        type: 'healing',
        score: 2,
        icon: 'fa-solid fa-mountain-sun',
      },
      {
        text: '유명 건축물과 전시, 역사 명소를 차례로 관람하는 일정',
        type: 'culture',
        score: 2,
        icon: 'fa-solid fa-building-columns',
      },
      {
        text: '오전부터 저녁까지 다양한 체험과 활동을 즐기는 일정',
        type: 'adventure',
        score: 2,
        icon: 'fa-solid fa-person-running',
      },
      {
        text: '정해진 목적지 없이 동네를 걷다가 마음에 드는 곳에 들어가는 일정',
        type: 'local',
        score: 2,
        icon: 'fa-solid fa-road',
      },
    ],
  },
  {
    id: 3,
    text: '여행 사진첩에 가장 많이 남기고 싶은 장면은?',
    options: [
      {
        text: '바다, 산, 노을처럼 마음이 편안해지는 풍경',
        type: 'healing',
        score: 2,
        icon: 'fa-solid fa-water',
      },
      {
        text: '전시 작품, 역사 유적, 독특한 건축물',
        type: 'culture',
        score: 2,
        icon: 'fa-solid fa-camera-retro',
      },
      {
        text: '새로운 활동에 도전하거나 친구들과 신나게 노는 모습',
        type: 'adventure',
        score: 2,
        icon: 'fa-solid fa-person-swimming',
      },
      {
        text: '오래된 골목, 작은 가게, 시장과 지역 주민의 일상',
        type: 'local',
        score: 2,
        icon: 'fa-solid fa-shop',
      },
    ],
  },
  {
    id: 4,
    text: '여행 중 예상보다 두 시간이 남았다면?',
    options: [
      {
        text: '가까운 공원이나 카페에서 쉬면서 풍경을 감상한다.',
        type: 'healing',
        score: 2,
        icon: 'fa-solid fa-mug-hot',
      },
      {
        text: '주변의 전시관이나 역사적인 장소를 찾아본다.',
        type: 'culture',
        score: 2,
        icon: 'fa-solid fa-palette',
      },
      {
        text: '현장에서 신청할 수 있는 체험 프로그램을 찾아본다.',
        type: 'adventure',
        score: 2,
        icon: 'fa-solid fa-ticket',
      },
      {
        text: '관광 안내에 잘 나오지 않는 골목과 동네를 돌아본다.',
        type: 'local',
        score: 2,
        icon: 'fa-solid fa-map',
      },
    ],
  },
  {
    id: 5,
    text: '여행을 다녀온 뒤 가장 만족스러운 순간은?',
    options: [
      {
        text: '복잡한 일상을 잊고 충분히 쉬었다고 느낄 때',
        type: 'healing',
        score: 3,
        icon: 'fa-solid fa-spa',
      },
      {
        text: '새로운 문화와 지역의 이야기를 알게 되었을 때',
        type: 'culture',
        score: 3,
        icon: 'fa-solid fa-book-open',
      },
      {
        text: '평소 해보지 못한 활동에 도전했을 때',
        type: 'adventure',
        score: 3,
        icon: 'fa-solid fa-medal',
      },
      {
        text: '나만 알고 싶은 특별한 장소를 발견했을 때',
        type: 'local',
        score: 3,
        icon: 'fa-solid fa-location-dot',
      },
    ],
  },
  {
    id: 6,
    text: '여행지를 고를 때 더 끌리는 장소는?',
    options: [
      {
        text: 'SNS에서 자주 보던 유명한 핫플은 꼭 가본다.',
        trait: 'hotplace',
        value: 2,
        icon: 'fa-solid fa-fire',
      },
      {
        text: '지역을 대표하는 인기 관광지를 우선 방문한다.',
        trait: 'hotplace',
        value: 1,
        icon: 'fa-solid fa-star',
      },
      {
        text: '지역 주민이 추천하는 덜 알려진 장소가 좋다.',
        trait: 'hotplace',
        value: -1,
        icon: 'fa-solid fa-map-pin',
      },
      {
        text: '검색해도 정보가 많지 않은 조용한 장소가 좋다.',
        trait: 'hotplace',
        value: -2,
        icon: 'fa-solid fa-location-crosshairs',
      },
    ],
  },
  {
    id: 7,
    text: '꼭 가보고 싶던 맛집의 대기 시간이 50분이라면?',
    options: [
      {
        text: '유명한 곳이라면 한 시간도 기다릴 수 있다.',
        trait: 'waiting',
        value: 2,
        icon: 'fa-solid fa-hourglass-half',
      },
      {
        text: '30분 정도까지는 기다려 본다.',
        trait: 'waiting',
        value: 1,
        icon: 'fa-regular fa-clock',
      },
      {
        text: '10분 이상 기다려야 한다면 다른 곳을 찾는다.',
        trait: 'waiting',
        value: -1,
        icon: 'fa-solid fa-person-walking-arrow-right',
      },
      {
        text: '처음부터 웨이팅이 없는 장소를 찾아간다.',
        trait: 'waiting',
        value: -2,
        icon: 'fa-solid fa-bolt',
      },
    ],
  },
  {
    id: 8,
    text: '관광지에 사람이 많을 때 나는?',
    options: [
      {
        text: '활기찬 분위기가 여행 온 기분을 더해준다.',
        trait: 'crowd',
        value: 2,
        icon: 'fa-solid fa-people-group',
      },
      {
        text: '인기 있는 장소라면 사람이 많아도 괜찮다.',
        trait: 'crowd',
        value: 1,
        icon: 'fa-solid fa-users',
      },
      {
        text: '사람이 적은 시간대를 골라 다시 방문한다.',
        trait: 'crowd',
        value: -1,
        icon: 'fa-regular fa-clock',
      },
      {
        text: '바로 다른 한적한 장소로 이동한다.',
        trait: 'crowd',
        value: -2,
        icon: 'fa-solid fa-tree',
      },
    ],
  },
  {
    id: 9,
    text: '여행 일정을 준비하는 나의 방식은?',
    options: [
      {
        text: '시간과 이동 경로까지 세세하게 계획한다.',
        trait: 'planning',
        value: 2,
        icon: 'fa-solid fa-calendar-check',
      },
      {
        text: '꼭 갈 장소와 식당 정도는 미리 정한다.',
        trait: 'planning',
        value: 1,
        icon: 'fa-solid fa-list-check',
      },
      {
        text: '대략적인 방향만 정하고 현장에서 바꾼다.',
        trait: 'planning',
        value: -1,
        icon: 'fa-solid fa-route',
      },
      {
        text: '당일의 기분과 상황에 따라 결정한다.',
        trait: 'planning',
        value: -2,
        icon: 'fa-solid fa-shuffle',
      },
    ],
  },
  {
    id: 10,
    text: '하루 여행에서 가장 만족스러운 일정은?',
    options: [
      {
        text: '최대한 많은 명소를 둘러보는 일정',
        trait: 'pace',
        value: 2,
        icon: 'fa-solid fa-forward-fast',
      },
      {
        text: '대표 장소 3~4곳을 알차게 보는 일정',
        trait: 'pace',
        value: 1,
        icon: 'fa-solid fa-map-location-dot',
      },
      {
        text: '한두 장소를 여유롭게 둘러보는 일정',
        trait: 'pace',
        value: -1,
        icon: 'fa-solid fa-person-walking',
      },
      {
        text: '마음에 드는 한 장소에서 오래 머무는 일정',
        trait: 'pace',
        value: -2,
        icon: 'fa-solid fa-couch',
      },
    ],
  },
]

const personalityTypes = {
  healing: {
    title: '자연 속 힐링 여행가',
    description:
      '복잡한 일정과 북적이는 장소보다 자연 속에서 천천히 쉬며 여유를 찾는 여행을 선호합니다.',
    icon: 'fa-solid fa-leaf',
    tags: ['자연', '휴식', '산책', '풍경'],
  },
  culture: {
    title: '도심 문화 탐방가',
    description:
      '지역의 역사와 문화, 전시와 건축물을 살펴보며 새로운 이야기를 알아가는 여행을 선호합니다.',
    icon: 'fa-solid fa-landmark',
    tags: ['문화', '전시', '역사', '도심'],
  },
  adventure: {
    title: '활동적인 모험 여행가',
    description:
      '여행지에서 직접 체험하고 움직이며 평소 해보지 못했던 새로운 활동에 도전하는 것을 즐깁니다.',
    icon: 'fa-solid fa-person-hiking',
    tags: ['체험', '레포츠', '도전', '활동'],
  },
  local: {
    title: '로컬 감성 여행가',
    description:
      '대표 관광지만 둘러보기보다 골목과 시장, 작은 가게처럼 지역의 생활과 분위기가 느껴지는 장소를 좋아합니다.',
    icon: 'fa-solid fa-store',
    tags: ['골목', '시장', '로컬', '숨은 명소'],
  },
}

const currentQuestion = computed(
  () => questions[currentQuestionIndex.value],
)

const selectedOptionIndex = computed(
  () => answers.value[currentQuestionIndex.value],
)

const progress = computed(() => {
  return ((currentQuestionIndex.value + 1) / questions.length) * 100
})

const resultType = ref(null)
const detailTags = ref([])

const result = computed(() => {
  if (!resultType.value) {
    return null
  }

  return personalityTypes[resultType.value]
})

function startTest() {
  testStarted.value = true
  testFinished.value = false
  currentQuestionIndex.value = 0
  answers.value = []
  resultType.value = null
  detailTags.value = []

  isMoving.value = false
  isSaving.value = false
  saveError.value = ''
}

function selectOption(optionIndex) {
  if (isMoving.value) {
    return
  }

  isMoving.value = true
  answers.value[currentQuestionIndex.value] = optionIndex

  setTimeout(async () => {
    if (currentQuestionIndex.value < questions.length - 1) {
      currentQuestionIndex.value += 1
      isMoving.value = false
      return
    }

    await calculateResult()
    isMoving.value = false
  }, 250)
}

function goToPreviousQuestion() {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value -= 1
  }
}

function getOrCreateClientId() {
  const savedClientId = localStorage.getItem('clientId')

  if (savedClientId) {
    return savedClientId
  }

  const newClientId = crypto.randomUUID()

  localStorage.setItem('clientId', newClientId)

  return newClientId
}

async function saveTravelProfile(traitScores) {
  const profileData = {
    client_id: getOrCreateClientId(),
    main_type: resultType.value,
    main_title: personalityTypes[resultType.value].title,
    traits: {
      hotplace: traitScores.hotplace,
      waiting: traitScores.waiting,
      crowd: traitScores.crowd,
      planning: traitScores.planning,
      pace: traitScores.pace,
    },
    tags: detailTags.value,
  }

  const response = await axios.post(
    `${API_BASE_URL}/api/profiles`,
    profileData,
  )

  console.log('여행 성향 저장 완료:', response.data)
}

async function calculateResult() {
  const mainScores = {
    healing: 0,
    culture: 0,
    adventure: 0,
    local: 0,
  }

  const traitScores = {
    hotplace: 0,
    waiting: 0,
    crowd: 0,
    planning: 0,
    pace: 0,
  }

  answers.value.forEach((optionIndex, questionIndex) => {
    const selectedOption =
      questions[questionIndex]?.options[optionIndex]

    if (!selectedOption) {
      return
    }

    // 1~5번 메인 성향 점수
    if (selectedOption.type) {
      mainScores[selectedOption.type] += selectedOption.score
    }

    // 6~10번 세부 성향 점수
    if (selectedOption.trait) {
      traitScores[selectedOption.trait] += selectedOption.value
    }
  })

  const highestScore = Math.max(...Object.values(mainScores))

  const highestTypes = Object.keys(mainScores).filter(
    (type) => mainScores[type] === highestScore,
  )

  // 메인 성향 동점 처리
  if (highestTypes.length > 1) {
    const fifthAnswerIndex = answers.value[4]
    const fifthAnswerType =
      questions[4].options[fifthAnswerIndex]?.type

    if (highestTypes.includes(fifthAnswerType)) {
      resultType.value = fifthAnswerType
    } else {
      const firstAnswerIndex = answers.value[0]
      const firstAnswerType =
        questions[0].options[firstAnswerIndex]?.type

      resultType.value = highestTypes.includes(firstAnswerType)
        ? firstAnswerType
        : highestTypes[0]
    }
  } else {
    resultType.value = highestTypes[0]
  }

  // 세부 성향 태그 결정
  detailTags.value = [
    traitScores.hotplace > 0
      ? '핫플선호'
      : '숨은명소선호',

    traitScores.waiting > 0
      ? '웨이팅가능'
      : '노웨이팅선호',

    traitScores.crowd > 0
      ? '활기찬분위기'
      : '한적한분위기',

    traitScores.planning > 0
      ? '계획형'
      : '즉흥형',

    traitScores.pace > 0
      ? '여러장소방문'
      : '한장소집중',
  ]

  isSaving.value = true
  saveError.value = ''

  try {
    await saveTravelProfile(traitScores)
  } catch (error) {
    console.error('여행 성향 저장 실패:', error)
    console.error('백엔드 응답:', error.response?.data)

    saveError.value =
      error.response?.data?.detail ||
      '성향 결과를 저장하지 못했습니다.'
  } finally {
    isSaving.value = false
    testFinished.value = true
  }
}

function restartTest() {
  startTest()
}
</script>

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
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
        >
          <i class="fa-solid fa-star mr-2"></i>
          추천
        </RouterLink>

        <RouterLink
          to="/board"
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
        >
          <i class="fa-regular fa-clipboard mr-2"></i>
          게시판
        </RouterLink>

        <RouterLink
          to="/map"
          class="rounded-full px-6 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
        >
          <i class="fa-solid fa-map-location-dot mr-2"></i>
          지도
        </RouterLink>
      </nav>
    </header>

    <main class="mx-auto mt-12 w-full max-w-3xl">
      <!-- 시작 화면 -->
      <section
        v-if="!testStarted"
        class="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-xl md:p-12"
      >
        <div
          class="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-sky-100 to-indigo-100 text-3xl text-sky-600"
        >
          <i class="fa-solid fa-compass"></i>
        </div>

        <p
          class="mt-8 text-sm font-bold uppercase tracking-wider text-sky-600"
        >
          Travel Personality Test
        </p>

        <h1 class="mt-3 text-3xl font-extrabold text-slate-900 md:text-4xl">
          나에게 어울리는 여행 스타일은?
        </h1>

        <p class="mx-auto mt-5 max-w-xl leading-relaxed text-slate-500">
          열 가지 질문을 통해 여행 성향과 핫플 선호도, 웨이팅 감수도,
          혼잡도와 일정 스타일을 분석합니다. 분석 결과는 챗봇의 맞춤형
          여행지 추천에 활용됩니다.
        </p>

        <button
          type="button"
          class="mt-8 rounded-2xl bg-gradient-to-r from-sky-500 to-indigo-600 px-8 py-4 font-bold text-white shadow-lg shadow-sky-500/20 transition hover:-translate-y-0.5 hover:shadow-xl"
          @click="startTest"
        >
          테스트 시작하기
          <i class="fa-solid fa-arrow-right ml-2"></i>
        </button>
      </section>

      <!-- 질문 화면 -->
      <section
        v-else-if="!testFinished"
        class="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl md:p-10"
      >
        <!-- 진행률 -->
        <div>
          <div class="flex items-center justify-between text-sm">
            <span class="font-semibold text-slate-500">
              {{ currentQuestionIndex + 1 }} / {{ questions.length }}
            </span>

            <span class="font-semibold text-sky-600">
              {{ Math.round(progress) }}%
            </span>
          </div>

          <div class="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
            <div
              class="h-full rounded-full bg-gradient-to-r from-sky-500 to-indigo-600 transition-all duration-300"
              :style="{ width: `${progress}%` }"
            ></div>
          </div>
        </div>

        <!-- 질문 -->
        <div class="mt-10">
          <p class="text-sm font-bold text-sky-600">
            QUESTION {{ currentQuestion.id }}
          </p>

          <h1
            class="mt-3 text-2xl font-extrabold leading-snug text-slate-900 md:text-3xl"
          >
            {{ currentQuestion.text }}
          </h1>
        </div>

        <!-- 선택지 -->
        <div class="mt-8 space-y-3">
          <button
            v-for="(option, optionIndex) in currentQuestion.options"
            :key="option.text"
            type="button"
            :disabled="isMoving"
            :class="[
              'flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition disabled:cursor-not-allowed disabled:opacity-70 md:p-5',
              selectedOptionIndex === optionIndex
                ? 'border-sky-500 bg-sky-50 ring-2 ring-sky-100'
                : 'border-slate-200 bg-white hover:border-sky-300 hover:bg-slate-50',
            ]"
            @click="selectOption(optionIndex)"
          >
            <div
              :class="[
                'flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-xl text-lg',
                selectedOptionIndex === optionIndex
                  ? 'bg-sky-500 text-white'
                  : 'bg-slate-100 text-slate-500',
              ]"
            >
              <i :class="option.icon"></i>
            </div>

            <span class="font-semibold text-slate-700">
              {{ option.text }}
            </span>

            <i
              v-if="selectedOptionIndex === optionIndex"
              class="fa-solid fa-circle-check ml-auto text-sky-500"
            ></i>
          </button>
        </div>

        <!-- 이전 / 다음 버튼 -->
        <div class="mt-8 flex items-center justify-between">
          <button
            type="button"
            class="rounded-xl px-5 py-3 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-30"
            :disabled="currentQuestionIndex === 0"
            @click="goToPreviousQuestion"
          >
            <i class="fa-solid fa-arrow-left mr-2"></i>
            이전
          </button>

          <p class="text-sm text-slate-400">
            선택하면 다음 질문으로 이동합니다.
          </p>
        </div>
      </section>

      <!-- 결과 화면 -->
      <section
        v-else-if="result"
        class="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-xl md:p-12"
      >
        <p class="text-sm font-bold uppercase tracking-wider text-sky-600">
          Your Travel Type
        </p>

        <div
          class="mx-auto mt-6 flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-sky-100 to-indigo-100 text-4xl text-sky-600"
        >
          <i :class="result.icon"></i>
        </div>

        <h1 class="mt-6 text-3xl font-extrabold text-slate-900 md:text-4xl">
          {{ result.title }}
        </h1>

        <p
          class="mx-auto mt-5 max-w-xl leading-relaxed text-slate-500"
        >
          {{ result.description }}
        </p>

        <!-- 메인 성향 키워드 -->
        <div class="mt-7 flex flex-wrap justify-center gap-2">
          <span
            v-for="tag in result.tags"
            :key="tag"
            class="rounded-full bg-sky-50 px-4 py-2 text-sm font-semibold text-sky-700"
          >
            #{{ tag }}
          </span>
        </div>

        <!-- 세부 여행 스타일 -->
        <div class="mt-8 rounded-2xl border border-slate-200 bg-slate-50 p-6">
          <h2 class="font-bold text-slate-900">
            나의 세부 여행 스타일
          </h2>

          <div class="mt-4 flex flex-wrap justify-center gap-2">
            <span
              v-for="tag in detailTags"
              :key="tag"
              class="rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-semibold text-indigo-700"
            >
              #{{ tag }}
            </span>
          </div>
        </div>

        <div
          class="mt-10 rounded-2xl border border-slate-200 bg-slate-50 p-6 text-left"
        >
          <h2 class="font-bold text-slate-900">
            맞춤 추천에 성향이 반영됩니다
          </h2>

          <p class="mt-2 text-sm leading-relaxed text-slate-500">
            저장된 여행 성향은 챗봇이 관광지와 여행 코스를 추천할 때
            활용됩니다. 같은 질문을 하더라도 핫플 선호도, 웨이팅 감수도,
            혼잡도와 일정 스타일에 따라 다른 추천을 받을 수 있습니다.
          </p>
        </div>
        <p
          v-if="saveError"
          class="mt-5 rounded-xl bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-600"
        >
          <i class="fa-solid fa-circle-exclamation mr-2"></i>
          {{ saveError }}
        </p>

        <p
          v-else
          class="mt-5 rounded-xl bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-700"
        >
          <i class="fa-solid fa-circle-check mr-2"></i>
          여행 성향이 저장되었습니다.
        </p>

        <div class="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
          <button
            type="button"
            class="rounded-xl border border-slate-200 px-6 py-3 font-semibold text-slate-600 transition hover:bg-slate-100"
            @click="restartTest"
          >
            <i class="fa-solid fa-rotate-right mr-2"></i>
            다시 테스트하기
          </button>

          <RouterLink
            to="/map"
            class="rounded-xl bg-slate-900 px-6 py-3 font-semibold text-white transition hover:bg-slate-700"
          >
            추천 장소 보러 가기
            <i class="fa-solid fa-map-location-dot ml-2"></i>
          </RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>