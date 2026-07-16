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