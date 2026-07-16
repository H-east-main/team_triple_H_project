<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'

// Local-only ChatBot: no backend calls. Simulates AI replies locally.

const messages = ref([
  { id: Date.now(), role: 'ai', text: '안녕하세요! 어디로 떠나고 싶으신가요?', time: new Date().toISOString() },
])

const inputText = ref('')
const isSending = ref(false)
const errorMessage = ref('')
const bodyRef = ref(null)

function pushUser(text) {
  const item = { id: Date.now(), role: 'user', text, time: new Date().toISOString() }
  messages.value.push(item)
  // return the index of the newly pushed user message
  return messages.value.length - 1
}

function pushAi(text) {
  messages.value.push({ id: Date.now(), role: 'ai', text, time: new Date().toISOString() })
}

function generateAiReply(userText) {
  if (/바다|해변/.test(userText)) return '조용한 바다를 원하시는군요. 한적한 해변 몇 곳을 추천해 드릴게요.'
  if (/산|등산|트레킹/.test(userText)) return '산을 좋아하시네요. 초보자 코스도 추천드립니다.'
  if (/맛집|음식|떡갈비/.test(userText)) return '맛집을 찾으시는군요. 지역별 베스트 몇 곳을 안내할게요.'
  return '좋아요! 원하시는 분위기(조용한/활기찬)나 지역을 알려주시면 더 정확히 추천해 드릴게요.'
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_URL = `${API_BASE_URL}/chat`
const SEARCH_URL = `${API_BASE_URL}/api/search`
const DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=60'
const searchResults = ref([])
const searchError = ref('')

async function send() {
  const text = inputText.value.trim()
  if (!text || isSending.value) return

  errorMessage.value = ''
  // push the user message and get its index
  const userIdx = pushUser(text)
  inputText.value = ''

  // add loading placeholder immediately after the user's message so user box stays
  isSending.value = true
  const loadingId = Date.now()
  const loadingBubble = { id: loadingId, role: 'ai', text: '응답을 생성 중입니다...', time: new Date().toISOString() }
  // insert loading bubble right after the user's message index
  messages.value.splice(userIdx + 1, 0, loadingBubble)

  try {
    const resp = await axios.post(API_URL, { question: text }, { timeout: 15000 })
    const answer = resp?.data?.answer
    const idx = messages.value.findIndex((m) => m.id === loadingId)
    // Normalize answer: if backend returned a stringified SDK Response, try
    // to extract the assistant's textual content from it.
    const rawOut = typeof answer === 'string' ? answer : String(answer ?? '')
    const out = extractAssistantText(rawOut) || rawOut
    if (idx !== -1) {
      // remove the loading placeholder and append a final AI response bubble
      messages.value.splice(idx, 1)
      pushAi(out)
    } else {
      pushAi(out)
    }
    // Fetch related places to display as cards below the chat (non-blocking)
    try {
      searchError.value = ''
      const sr = await axios.post(SEARCH_URL, { q: text, max: 10 }, { timeout: 8000 })
      searchResults.value = Array.isArray(sr.data?.results) ? sr.data.results : []
    } catch (se) {
      console.error('Search fetch error:', se)
      searchResults.value = []
      searchError.value = '검색된 장소를 불러오지 못했습니다.'
    }
  } catch (err) {
    console.error('Chat send error:', err)
    errorMessage.value = '서버 요청 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'
    const idx = messages.value.findIndex((m) => m.id === loadingId)
    if (idx !== -1) {
      // remove loading placeholder and show an error response bubble
      messages.value.splice(idx, 1)
      pushAi('응답을 받을 수 없습니다.')
    }
  } finally {
    isSending.value = false
  }
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

// Try to extract assistant text from a stringified SDK Response object.
// Returns extracted text or null if none found.
function extractAssistantText(s) {
  if (!s || typeof s !== 'string') return null

  // Pattern 1: python repr style: text='...'
  let m = s.match(/text=\'([\s\S]*?)\'/)
  if (m && m[1]) return m[1]

  // Pattern 2: JSON-like "text": "..."
  m = s.match(/"text"\s*:\s*"([\s\S]*?)"/)
  if (m && m[1]) return m[1]

  // Pattern 3: look for common phrase 'I didn'\'t understand' or other English content
  // fallback: extract after "content=[" occurrences
  m = s.match(/content=\[.*?text=\'([\s\S]*?)\'/)
  if (m && m[1]) return m[1]

  return null
}

async function scrollToBottom() {
  await nextTick()
  const el = bodyRef.value
  if (el) {
    try {
      el.scrollTop = el.scrollHeight
    } catch (e) {
      // ignore
    }
  }
}

watch(messages, () => {
  void scrollToBottom()
})

onMounted(() => {
  void scrollToBottom()
})
</script>

<template>
  <div class="chatbot-root">
    <div class="chat-header">
      <strong>여행 챗봇</strong>
    </div>

    <div class="chat-body" ref="bodyRef">
      <div v-for="msg in messages" :key="msg.id" :class="['chat-message', msg.role]">
        <div class="bubble">
          <p class="text">{{ msg.text }}</p>
          <time class="time">{{ new Date(msg.time).toLocaleTimeString('ko-KR') }}</time>
        </div>
      </div>
    </div>

    <!-- Recommendation cards commented out per request
    <div v-if="searchResults.length" class="cards-container">
      <div v-for="place in searchResults" :key="place.id" class="card">
        <img :src="place.image || DEFAULT_IMAGE" alt="place image" class="card-img" />
        <div class="card-body">
          <h4 class="card-title">{{ place.title }}</h4>
          <p class="card-address">{{ place.address }}</p>
          <p class="card-category">{{ place.category }}</p>
          <button class="card-btn" @click="() => window.open('#', '_blank')">자세히 보기</button>
        </div>
      </div>
    </div>
    -->

    <div class="chat-input">
      <textarea
        v-model="inputText"
        @keydown="handleKeydown"
        placeholder="메시지를 입력하고 Enter로 전송 (Shift+Enter 줄바꿈)"
        rows="1"
      ></textarea>

      <button class="send-btn" :disabled="isSending || !inputText.trim()" @click="send">
        <span v-if="isSending">로딩...</span>
        <span v-else>전송</span>
      </button>
    </div>

    <div v-if="errorMessage" class="chat-error">{{ errorMessage }}</div>
  </div>
</template>

<style scoped>
.chatbot-root {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 30px rgba(2,6,23,0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(15, 23, 42, 0.06);
}

.chat-header {
  padding: 12px 16px;
  background: linear-gradient(90deg, #06b6d4, #6366f1);
  color: white;
  font-size: 14px;
}

.chat-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 320px;
  overflow: auto;
  background: linear-gradient(180deg, #f8fafc, #fff);
}

.chat-message {
  display: flex;
  width: 100%;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.ai {
  justify-content: flex-start;
}

.bubble {
  max-width: 78%;
  padding: 10px 12px;
  border-radius: 12px;
  display: inline-flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(2,6,23,0.06);
}

.chat-message.user .bubble { align-self: flex-end; }
.chat-message.ai .bubble { align-self: flex-start; }

.chat-message.user .bubble {
  background: linear-gradient(90deg, #0ea5a4, #6366f1);
  color: white;
  border-bottom-right-radius: 6px;
}

.chat-message.ai .bubble {
  background: #f1f5f9;
  color: #0f172a;
  border-bottom-left-radius: 6px;
}

.text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 13px;
}

.time {
  margin-top: 6px;
  font-size: 11px;
  opacity: 0.6;
  align-self: flex-end;
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 10px;
  border-top: 1px solid rgba(15, 23, 42, 0.04);
  background: #ffffff;
}

.chat-input textarea {
  flex: 1;
  resize: none;
  border: 1px solid rgba(15,23,42,0.06);
  padding: 10px 12px;
  border-radius: 10px;
  font-size: 13px;
  min-height: 38px;
  background: #fff;
}

.send-btn {
  background: #0f172a;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-error {
  margin-top: 8px;
  color: #b91c1c;
  font-size: 13px;
  text-align: center;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  padding: 12px;
  border-top: 1px solid rgba(15,23,42,0.04);
  background: #fff;
}

.card {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(2,6,23,0.04);
  border: 1px solid rgba(15,23,42,0.04);
}

.card-img {
  width: 100%;
  height: 110px;
  object-fit: cover;
}

.card-body {
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-title {
  font-size: 14px;
  margin: 0;
  font-weight: 700;
}

.card-address, .card-category {
  font-size: 12px;
  color: #475569;
  margin: 0;
}

.card-btn {
  margin-top: 6px;
  align-self: flex-start;
  background: #0f172a;
  color: #fff;
  border: none;
  padding: 6px 10px;
  border-radius: 8px;
  cursor: pointer;
}

</style>
