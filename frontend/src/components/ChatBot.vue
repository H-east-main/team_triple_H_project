<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const emit = defineEmits(['places-updated'])

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const CHAT_URL = `${API_BASE_URL}/chat`
const SEARCH_URL = `${API_BASE_URL}/api/search`

const question = ref('')
const loading = ref(false)
const errorMessage = ref('')
const chatBody = ref(null)

const messages = ref([
  {
    id: Date.now(),
    role: 'assistant',
    content: '안녕하세요! 어디로 떠나고 싶으신가요?',
  },
])

function createMessage(role, content) {
  return {
    id: `${Date.now()}-${Math.random()}`,
    role,
    content,
  }
}

async function scrollBottom() {
  await nextTick()

  if (!chatBody.value) {
    return
  }

  chatBody.value.scrollTop = chatBody.value.scrollHeight
}

function extractAssistantText(answer) {
  if (typeof answer !== 'string') {
    return String(answer ?? '')
  }

  // 일반 문자열 응답이면 그대로 사용
  if (
    !answer.includes("text='") &&
    !answer.includes('"text"')
  ) {
    return answer
  }

  // Python 객체 문자열 형태: text='답변'
  let match = answer.match(/text='([\s\S]*?)'/)

  if (match?.[1]) {
    return match[1]
  }

  // JSON 문자열 형태: "text": "답변"
  match = answer.match(/"text"\s*:\s*"([\s\S]*?)"/)

  if (match?.[1]) {
    return match[1]
  }

  return answer
}

function normalizePlaces(results) {
  if (!Array.isArray(results)) {
    return []
  }

  return results
    .map((place, index) => {
      const latitude = Number(
        place.latitude ??
          place.lat ??
          place.mapy,
      )

      const longitude = Number(
        place.longitude ??
          place.lng ??
          place.mapx,
      )

      return {
        ...place,

        id:
          place.id ??
          place.contentid ??
          `place-${index}`,

        title:
          place.title ??
          place.name ??
          `추천 장소 ${index + 1}`,

        address:
          place.address ??
          place.addr1 ??
          '',

        latitude,
        longitude,

        order: index + 1,
      }
    })
    .filter((place) => {
      return (
        Number.isFinite(place.latitude) &&
        Number.isFinite(place.longitude) &&
        place.latitude !== 0 &&
        place.longitude !== 0
      )
    })
}

async function fetchRecommendedPlaces(userQuestion) {
  try {
    const response = await axios.post(
      SEARCH_URL,
      {
        q: userQuestion,
        max: 10,
      },
      {
        timeout: 8000,
      },
    )

    const places = normalizePlaces(
      response.data?.results,
    )

    // 부모 컴포넌트로 지도에 표시할 장소 전달
    emit('places-updated', places)
  } catch (error) {
    console.error('장소 검색 오류:', error)

    // 검색 실패 시 기존 지도 경로 제거
    emit('places-updated', [])
  }
}

async function sendMessage() {
  const userQuestion = question.value.trim()

  if (!userQuestion || loading.value) {
    return
  }

  messages.value.push(
    createMessage('user', userQuestion),
  )

  question.value = ''
  errorMessage.value = ''
  loading.value = true

  await scrollBottom()

  try {
    const response = await axios.post(
      CHAT_URL,
      {
        question: userQuestion,
      },
      {
        timeout: 15000,
      },
    )

    const answer = extractAssistantText(
      response.data?.answer,
    )

    messages.value.push(
      createMessage(
        'assistant',
        answer || '답변 내용을 불러오지 못했습니다.',
      ),
    )

    await scrollBottom()

    // 챗봇 질문을 기준으로 관련 장소 검색
    await fetchRecommendedPlaces(userQuestion)
  } catch (error) {
    console.error('챗봇 요청 오류:', error)

    errorMessage.value =
      '서버 요청 중 오류가 발생했습니다.'

    messages.value.push(
      createMessage(
        'assistant',
        '서버와 연결할 수 없습니다.',
      ),
    )

    emit('places-updated', [])
  } finally {
    loading.value = false
    await scrollBottom()
  }
}

function handleKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    void sendMessage()
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="header">
      여행 챗봇
    </div>

    <div
      ref="chatBody"
      class="body"
    >
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['row', msg.role]"
      >
        <div :class="['bubble', msg.role]">
          {{ msg.content }}
        </div>
      </div>

      <div
        v-if="loading"
        class="row assistant"
      >
        <div class="bubble assistant">
          응답을 생성 중입니다...
        </div>
      </div>
    </div>

    <div class="footer">
      <textarea
        v-model="question"
        placeholder="메시지를 입력하세요."
        rows="1"
        :disabled="loading"
        @keydown="handleKeydown"
      ></textarea>

      <button
        :disabled="loading || !question.trim()"
        @click="sendMessage"
      >
        {{ loading ? '로딩...' : '전송' }}
      </button>
    </div>

    <p
      v-if="errorMessage"
      class="error-message"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<style scoped>
.chat-container {
  width: 420px;
  height: 580px;
  margin: auto;
  display: flex;
  flex-direction: column;
  border-radius: 15px;
  overflow: hidden;
  background: white;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.header {
  padding: 15px;
  color: white;
  font-size: 20px;
  font-weight: bold;
  background: linear-gradient(90deg, #14b8d4, #6366f1);
}

.body {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f8fafc;
}

.row {
  display: flex;
  margin-bottom: 15px;
}

.row.user {
  justify-content: flex-end;
}

.row.assistant {
  justify-content: flex-start;
}

.bubble {
  max-width: 70%;
  padding: 12px;
  border-radius: 15px;
  white-space: pre-wrap;
  word-break: break-word;
}

.bubble.user {
  color: white;
  background: linear-gradient(90deg, #14b8d4, #6366f1);
}

.bubble.assistant {
  color: #0f172a;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.footer {
  display: flex;
  gap: 10px;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.footer textarea {
  flex: 1;
  min-height: 42px;
  padding: 10px 12px;
  border: 2px solid orange;
  border-radius: 10px;
  outline: none;
  resize: none;
  font-family: inherit;
}

.footer textarea:disabled {
  background: #f1f5f9;
}

.footer button {
  width: 80px;
  border: none;
  border-radius: 10px;
  color: white;
  background: #64748b;
  cursor: pointer;
}

.footer button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  margin: 0;
  padding: 0 12px 10px;
  color: #b91c1c;
  font-size: 13px;
  text-align: center;
}
</style>