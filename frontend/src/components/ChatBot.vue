<template>
  <div class="chat-container">
    <div class="chat-column">
      <div class="header">여행 챗봇</div>

      <div class="body" ref="chatBody">
        <div v-for="(msg,index) in messages" :key="index" :class="['row', msg.role]">
          <div :class="['bubble', msg.role]">{{ msg.content }}</div>
        </div>

        <div class="row assistant" v-if="loading">
          <div class="bubble assistant">응답을 생성 중입니다...</div>
        </div>
      </div>

      <div class="footer">
        <input v-model="question" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요." />
        <button @click="sendMessage" :disabled="loading">{{ loading ? '로딩...' : '전송' }}</button>
      </div>
    </div>

    <div class="cards-column">
      <div v-if="places && places.length" class="cards-title">추천 장소</div>
      <div v-if="places && places.length" class="cards-grid">
        <div v-for="place in places" :key="place.id" class="card">
          <img :src="place.image || defaultImage" class="card-img" alt="place" />
          <div class="card-body">
            <div class="card-title">{{ place.title }}</div>
            <div class="card-address">{{ place.address }}</div>
            <div class="card-category">{{ place.category }}</div>
            <button class="card-btn" @click="openMap(place)">자세히 보기</button>
          </div>
        </div>
      </div>
      <div v-else class="cards-empty">추천 장소가 없습니다.</div>
    </div>

    <!-- Modal map -->
    <div v-if="showMap" class="modal-overlay" @click.self="closeMap">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ mapTitle }}</h3>
          <button class="modal-close" @click="closeMap">✕</button>
        </div>
        <div class="modal-body">
          <iframe :src="mapSrc" frameborder="0" style="width:100%;height:360px"></iframe>
          <p class="modal-address">{{ mapAddress }}</p>
        </div>
      </div>
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

// places returned alongside chat response
const places = ref([])
const defaultImage = 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=60'

// modal map state
const showMap = ref(false)
const mapSrc = ref('')
const mapAddress = ref('')
const mapTitle = ref('')

function openMap(place){
  mapTitle.value = place.title || ''
  mapAddress.value = place.address || ''
  const q = encodeURIComponent(mapAddress.value || place.title || '')
  mapSrc.value = `https://www.google.com/maps?q=${q}&output=embed`
  showMap.value = true
}

function closeMap(){
  showMap.value = false
  mapSrc.value = ''
}

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
    // populate places if provided
    places.value = Array.isArray(res.data.places) ? res.data.places : []

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
  width: 100%;
  max-width: 920px;
  height: 80vh;
  max-height: 800px;

  margin:auto;

  display:flex;
  flex-direction:row;

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
  flex:1 1 auto;
  min-height: 0;
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

/* right column cards */
.chat-column{ flex:1 1 0; display:flex; flex-direction:column }
.cards-column{ width:340px; flex:0 0 340px; padding:16px; background:#fff; overflow:auto }
.cards-title{ font-weight:700; margin-bottom:8px }
.cards-grid{ display:grid; grid-template-columns:1fr 1fr; gap:12px }
.card{ border:1px solid rgba(0,0,0,0.06); border-radius:8px; overflow:hidden; background:#fff }
.card-img{ width:100%; height:100px; object-fit:cover }
.card-body{ padding:8px }
.card-btn{ background:#0f172a; color:#fff; padding:6px 8px; border:none; border-radius:6px; cursor:pointer }

/* modal */
.modal-overlay{ position:fixed; inset:0; background:rgba(0,0,0,0.4); display:flex; align-items:center; justify-content:center; z-index:50 }
.modal{ background:#fff; width:90%; max-width:720px; border-radius:8px; overflow:hidden }
.modal-header{ display:flex; justify-content:space-between; align-items:center; padding:12px; border-bottom:1px solid #eee }
.modal-body{ padding:12px }
.modal-address{ margin-top:8px; color:#374151 }
.modal-close{ background:transparent; border:none; font-size:18px; cursor:pointer }

</style>
