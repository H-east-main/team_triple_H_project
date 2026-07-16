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
  <div class="chat-container">

    <div class="header">
      여행 챗봇
    </div>

    <div class="body" ref="chatBody">

      <div
        v-for="(msg,index) in messages"
        :key="index"
        :class="['row',msg.role]"
      >
        <div :class="['bubble',msg.role]">
          {{ msg.content }}
        </div>
      </div>

      <div
        class="row assistant"
        v-if="loading"
      >
        <div class="bubble assistant">
          응답을 생성 중입니다...
        </div>
      </div>

    </div>

    <div class="footer">

      <input
        v-model="question"
        @keyup.enter="sendMessage"
        placeholder="메시지를 입력하세요."
      />

      <button
        @click="sendMessage"
        :disabled="loading"
      >
        {{ loading ? "로딩..." : "전송" }}
      </button>

    </div>

  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import axios from "axios";

const question = ref("");

const loading = ref(false);

const chatBody = ref(null);

const messages = ref([
  {
    role: "assistant",
    content: "안녕하세요! 어디로 떠나고 싶으신가요?"
  }
]);

function scrollBottom() {

  nextTick(() => {

    chatBody.value.scrollTop =
      chatBody.value.scrollHeight;

  });

}

async function sendMessage() {

  if (!question.value.trim()) return;

  const userQuestion = question.value;

  messages.value.push({
    role: "user",
    content: userQuestion
  });

  question.value = "";

  scrollBottom();

  loading.value = true;

  try {

    const res = await axios.post(
      "http://localhost:8000/chat",
      {
        question: userQuestion
      }
    );

    messages.value.push({
      role: "assistant",
      content: res.data.answer
    });

  } catch (e) {

    messages.value.push({
      role: "assistant",
      content: "서버와 연결할 수 없습니다."
    });

    console.error(e);

  } finally {

    loading.value = false;

    scrollBottom();

  }

}
</script>

<style scoped>

.chat-container{

  width:420px;
  height:580px;

  margin:auto;

  display:flex;
  flex-direction:column;

  border-radius:15px;

  overflow:hidden;

  box-shadow:0 5px 20px rgba(0,0,0,.15);

}

.header{

  background:linear-gradient(90deg,#14b8d4,#6366f1);

  color:white;

  padding:15px;

  font-size:20px;

  font-weight:bold;

}

.body{

  flex:1;

  padding:15px;

  overflow-y:auto;

  background:#f8fafc;

}

.row{

  display:flex;

  margin-bottom:15px;

}

.row.user{

  justify-content:flex-end;

}

.row.assistant{

  justify-content:flex-start;

}

.bubble{

  max-width:70%;

  padding:12px;

  border-radius:15px;

  white-space:pre-wrap;

}

.bubble.user{

  color:white;

  background:linear-gradient(90deg,#14b8d4,#6366f1);

}

.bubble.assistant{

  background:white;

  box-shadow:0 2px 8px rgba(0,0,0,.1);

}

.footer{

  display:flex;

  padding:10px;

  border-top:1px solid #ddd;

}

.footer input{

  flex:1;

  height:42px;

  border:2px solid orange;

  border-radius:10px;

  padding-left:12px;

  outline:none;

}

.footer button{

  margin-left:10px;

  width:80px;

  border:none;

  background:#9ca3af;

  color:white;

  border-radius:10px;

  cursor:pointer;

}

.footer button:disabled{

  cursor:not-allowed;

}

</style>