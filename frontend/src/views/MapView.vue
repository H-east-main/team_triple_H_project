<template>
  <div class="min-h-screen bg-slate-50 p-4 text-slate-800 antialiased md:p-10">
    <!-- 상단 메뉴 -->
    <header class="mx-auto flex w-full max-w-7xl justify-center">
      <nav
        class="flex gap-1 rounded-full border border-slate-200 bg-white/80 px-2 py-1.5 shadow-sm backdrop-blur-md"
      >
        <RouterLink
          to="/"
          class="rounded-full px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 md:px-6"
        >
          <i class="fa-solid fa-star mr-2"></i>
          추천
        </RouterLink>

        <RouterLink
          to="/board"
          class="rounded-full px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 md:px-6"
        >
          <i class="fa-regular fa-clipboard mr-2"></i>
          게시판
        </RouterLink>

        <RouterLink
          to="/map"
          class="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm md:px-6"
        >
          <i class="fa-solid fa-map-location-dot mr-2"></i>
          지도
        </RouterLink>
      </nav>
    </header>

    <main class="mx-auto mt-10 max-w-7xl">
      <!-- 제목 -->
      <section class="mb-7">
        <div
          class="mb-4 inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-bold text-emerald-700"
        >
          <i class="fa-solid fa-location-dot"></i>
          광주·전라 여행지도
        </div>

        <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 class="text-3xl font-extrabold tracking-tight md:text-4xl">
              여행지를 지도에서 둘러보세요
            </h1>

            <p class="mt-3 text-slate-500">
              관광지, 맛집, 축제와 여행코스를 선택하여 지도에서 확인할 수 있습니다.
            </p>
          </div>

          <button
            type="button"
            class="self-start rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 md:self-auto"
            @click="resetMap"
          >
            <i class="fa-solid fa-rotate-right mr-2"></i>
            지도 초기화
          </button>
        </div>
      </section>

      <!-- 필터 -->
      <section class="mb-5 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center">
          <div class="flex items-center gap-2 text-sm font-bold text-slate-700">
            <i class="fa-solid fa-filter"></i>
            카테고리
          </div>

          <div class="flex flex-wrap gap-2">
            <button
              v-for="category in categories"
              :key="category.fileName"
              type="button"
              class="rounded-full border px-4 py-2 text-sm font-semibold transition"
              :class="
                selectedCategory.fileName === category.fileName
                  ? 'border-slate-900 bg-slate-900 text-white'
                  : 'border-slate-200 hover:bg-slate-100'
              "
              @click="selectCategory(category)"
            >
              <i :class="[category.icon, 'mr-2']"></i>
              {{ category.label }}
            </button>
          </div>

          <!-- 검색 -->
          <div class="flex w-full gap-2 lg:ml-auto lg:w-auto">
            <div class="relative flex-1 lg:w-64">
              <i
                class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-sm text-slate-400"
              ></i>

              <input
                v-model="searchKeyword"
                type="text"
                placeholder="지역 또는 장소 검색"
                class="w-full rounded-xl border border-slate-200 py-2.5 pl-10 pr-4 text-sm outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-900/10"
                @keydown.enter="searchPlaces"
              />
            </div>

            <button
              type="button"
              class="rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-700"
              @click="searchPlaces"
            >
              검색
            </button>
          </div>
        </div>
      </section>

      <!-- 상태 메시지 -->
      <section
        v-if="status.message"
        class="mb-5 rounded-xl border px-4 py-3 text-sm font-semibold"
        :class="statusClass"
      >
        {{ status.message }}
      </section>

      <!-- 지도 + 목록 -->
      <section class="grid grid-cols-1 gap-5 lg:grid-cols-[1fr_340px]">
        <div
          class="relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm"
        >
          <div ref="mapElement" class="map-area"></div>

          <!-- 로딩 -->
          <div
            v-if="isLoading"
            class="absolute inset-0 z-20 flex items-center justify-center bg-white/80 backdrop-blur-sm"
          >
            <div class="text-center">
              <i class="fa-solid fa-spinner fa-spin text-3xl text-slate-800"></i>
              <p class="mt-3 text-sm font-semibold text-slate-600">
                지도 데이터를 불러오는 중입니다.
              </p>
            </div>
          </div>

          <!-- 표시 정보 -->
          <div
            class="absolute left-4 top-4 z-10 rounded-xl border border-slate-200 bg-white/90 px-4 py-3 shadow-sm backdrop-blur-md"
          >
            <p class="text-xs text-slate-500">현재 표시 중</p>
            <p class="mt-1 font-bold">
              <span>{{ currentCategoryLabel }}</span>
              <span class="mx-1 text-slate-400">·</span>
              <span>{{ filteredPlaces.length }}</span>개
            </p>
          </div>
        </div>

        <!-- 장소 목록 -->
        <aside class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div class="border-b border-slate-100 p-5">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-lg font-extrabold">장소 목록</h2>
                <p class="mt-1 text-xs text-slate-500">
                  장소를 클릭하면 지도에서 확인할 수 있어요.
                </p>
              </div>

              <i class="fa-solid fa-list text-slate-400"></i>
            </div>
          </div>

          <div class="place-list max-h-[555px] space-y-3 overflow-y-auto p-3">
            <div
              v-if="filteredPlaces.length === 0"
              class="py-16 text-center text-slate-400"
            >
              <i class="fa-solid fa-location-dot text-3xl"></i>
              <p class="mt-3 text-sm font-semibold">표시할 장소가 없습니다.</p>
              <p class="mt-1 text-xs">다른 카테고리나 검색어를 선택해보세요.</p>
            </div>

            <button
              v-for="(place, index) in filteredPlaces"
              :key="String(place.id)"
              :ref="(element) => setPlaceCardRef(place.id, element)"
              type="button"
              class="w-full rounded-2xl border p-3 text-left transition hover:border-slate-400 hover:bg-slate-50"
              :class="
                selectedPlaceId === String(place.id)
                  ? 'border-slate-900 bg-slate-50'
                  : 'border-slate-200'
              "
              @click="focusPlace(place.id)"
            >
              <div class="flex gap-3">
                <img
                  v-if="place.imageUrl && !brokenImageIds.has(String(place.id))"
                  :src="place.imageUrl"
                  :alt="place.title"
                  class="h-20 w-20 shrink-0 rounded-xl object-cover"
                  @error="markImageBroken(place.id)"
                />

                <div
                  v-else
                  class="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-400"
                >
                  <i class="fa-regular fa-image text-xl"></i>
                </div>

                <div class="min-w-0 flex-1">
                  <div class="flex items-start gap-2">
                    <span
                      class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-900 text-xs font-bold text-white"
                    >
                      {{ index + 1 }}
                    </span>

                    <h3 class="line-clamp-2 text-sm font-bold leading-5">
                      {{ place.title }}
                    </h3>
                  </div>

                  <p class="mt-2 line-clamp-2 text-xs text-slate-500">
                    {{ place.address || "주소 정보 없음" }}
                  </p>

                  <span
                    class="mt-2 inline-block rounded-full bg-slate-100 px-2 py-1 text-[11px] font-semibold text-slate-500"
                  >
                    {{ place.contentType }}
                  </span>
                </div>
              </div>
            </button>
          </div>
        </aside>
      </section>

      <!-- 추천 경로 -->
      <section
        v-if="routePlaces.length >= 2"
        class="mt-5 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        <div class="flex items-center justify-between gap-4">
          <div>
            <h2 class="text-xl font-extrabold">
              <i class="fa-solid fa-route mr-2"></i>
              추천 여행 경로
            </h2>

            <p class="mt-2 text-sm text-slate-500">
              사용자 성향을 기반으로 선택된 장소의 추천 방문 순서입니다.
            </p>
          </div>

          <button
            type="button"
            class="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold transition hover:bg-slate-100"
            @click="clearRoute"
          >
            경로 지우기
          </button>
        </div>

        <div class="mt-5 grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-4">
          <button
            v-for="(place, index) in routePlaces"
            :key="String(place.id)"
            type="button"
            class="rounded-2xl border border-slate-200 p-4 text-left transition hover:border-slate-400"
            @click="focusPlace(place.id)"
          >
            <div class="flex items-center gap-3">
              <span
                class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white"
              >
                {{ index + 1 }}
              </span>

              <strong class="line-clamp-2 text-sm leading-5">
                {{ place.title }}
              </strong>
            </div>

            <p
              v-if="place.recommendationReason"
              class="mt-2 text-xs text-slate-500"
            >
              {{ place.recommendationReason }}
            </p>
          </button>
        </div>

        <p class="mt-4 text-xs text-slate-400">
          현재 경로선은 추천 장소를 순서대로 연결한 시각화입니다. 실제 도로
          길찾기는 별도의 길찾기 API 연동이 필요합니다.
        </p>
      </section>
    </main>
  </div>
</template>

<script setup>
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  reactive,
  ref,
} from "vue";

const DATA_BASE_PATH = "/data/";
const DEFAULT_CENTER = {
  latitude: 35.1595,
  longitude: 126.8526,
};
const DEFAULT_LEVEL = 9;

const categories = [
  {
    label: "여행코스",
    fileName: "travel-courses.json",
    icon: "fa-solid fa-route",
  },
  {
    label: "관광지",
    fileName: "tourist-spots.json",
    icon: "fa-solid fa-mountain-sun",
  },
  {
    label: "맛집",
    fileName: "restaurants.json",
    icon: "fa-solid fa-utensils",
  },
  {
    label: "축제",
    fileName: "festivals.json",
    icon: "fa-solid fa-masks-theater",
  },
];

const mapElement = ref(null);
const selectedCategory = ref(categories[0]);
const currentCategoryLabel = ref(categories[0].label);
const currentPlaces = ref([]);
const filteredPlaces = ref([]);
const routePlaces = ref([]);
const selectedPlaceId = ref(null);
const searchKeyword = ref("");
const isLoading = ref(true);

const status = reactive({
  message: "",
  type: "success",
});

const brokenImageIds = reactive(new Set());
const placeCardRefs = new Map();

let map = null;
let markers = [];
let infoWindows = [];
let routePolyline = null;

const statusClass = computed(() => {
  const styles = {
    success: "border-emerald-200 bg-emerald-50 text-emerald-700",
    warning: "border-amber-200 bg-amber-50 text-amber-700",
    error: "border-red-200 bg-red-50 text-red-700",
  };

  return styles[status.type] ?? styles.success;
});

function setPlaceCardRef(placeId, element) {
  const key = String(placeId);

  if (element) {
    placeCardRefs.set(key, element);
  } else {
    placeCardRefs.delete(key);
  }
}

function markImageBroken(placeId) {
  brokenImageIds.add(String(placeId));
}

function showStatus(message, type = "success") {
  status.message = message;
  status.type = type;
}

function clearStatus() {
  status.message = "";
  status.type = "success";
}

function createRandomId() {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }

  return `${Date.now()}${Math.random().toString(16).slice(2)}`;
}

function normalizePlace(item, contentType) {
  return {
    id: item.contentid ?? item.id ?? createRandomId(),
    title: item.title ?? item.name ?? "이름 없는 장소",
    address: [item.addr1, item.addr2].filter(Boolean).join(" "),
    longitude: Number(item.mapx ?? item.longitude),
    latitude: Number(item.mapy ?? item.latitude),
    imageUrl: item.firstimage || item.firstimage2 || item.imageUrl || "",
    contentType: item.contentType || item.category || contentType,
    categoryCode: item.cat3 || item.categoryCode || "",
    telephone: item.tel || item.telephone || "",
    recommendationReason: item.recommendationReason || "",
    order: Number(item.order ?? item.recommendedOrder),
    original: item,
  };
}

function isValidCoordinate(place) {
  const { latitude, longitude } = place;

  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
    return false;
  }

  if (latitude === 0 || longitude === 0) {
    return false;
  }

  return (
    latitude >= 33 &&
    latitude <= 37 &&
    longitude >= 124 &&
    longitude <= 129
  );
}

async function loadJsonFile(fileName) {
  const response = await fetch(`${DATA_BASE_PATH}${fileName}`);

  if (!response.ok) {
    throw new Error(`${fileName} 파일을 불러오지 못했습니다.`);
  }

  const data = await response.json();

  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data.items)) {
    return data.items;
  }

  throw new Error(`${fileName}에서 items 배열을 찾을 수 없습니다.`);
}

function loadKakaoSdk() {
  return new Promise((resolve, reject) => {
    if (window.kakao?.maps) {
      window.kakao.maps.load(resolve);
      return;
    }

    const appKey = import.meta.env.VITE_KAKAO_JAVASCRIPT_KEY;

    if (!appKey) {
      reject(
        new Error(
          ".env에 VITE_KAKAO_JAVASCRIPT_KEY가 설정되어 있지 않습니다.",
        ),
      );
      return;
    }

    const existingScript = document.querySelector(
      'script[data-kakao-map-sdk="true"]',
    );

    if (existingScript) {
      existingScript.addEventListener("load", () => {
        window.kakao.maps.load(resolve);
      });
      existingScript.addEventListener("error", reject);
      return;
    }

    const script = document.createElement("script");
    script.dataset.kakaoMapSdk = "true";
    script.async = true;
    script.src =
  `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${encodeURIComponent(appKey)}`;

    script.onload = () => {
      if (!window.kakao?.maps) {
        reject(new Error("카카오맵 SDK 객체를 찾을 수 없습니다."));
        return;
      }

      window.kakao.maps.load(resolve);
    };

    script.onerror = () => {
      reject(new Error("카카오맵 SDK를 불러오지 못했습니다."));
    };

    document.head.appendChild(script);
  });
}

async function initializeKakaoMap() {
  try {
    await loadKakaoSdk();

    const mapOption = {
      center: new window.kakao.maps.LatLng(
        DEFAULT_CENTER.latitude,
        DEFAULT_CENTER.longitude,
      ),
      level: DEFAULT_LEVEL,
    };

    map = new window.kakao.maps.Map(mapElement.value, mapOption);
    addMapControls();
    await loadCategoryData(
      selectedCategory.value.fileName,
      selectedCategory.value.label,
    );
  } catch (error) {
    console.error(error);
    isLoading.value = false;
    showStatus(error.message || "카카오맵을 초기화하지 못했습니다.", "error");
  }
}

function addMapControls() {
  const mapTypeControl = new window.kakao.maps.MapTypeControl();
  map.addControl(
    mapTypeControl,
    window.kakao.maps.ControlPosition.TOPRIGHT,
  );

  const zoomControl = new window.kakao.maps.ZoomControl();
  map.addControl(zoomControl, window.kakao.maps.ControlPosition.RIGHT);
}

async function selectCategory(category) {
  selectedCategory.value = category;
  searchKeyword.value = "";
  routePlaces.value = [];
  clearRoute();

  await loadCategoryData(category.fileName, category.label);
}

async function loadCategoryData(fileName, contentType) {
  isLoading.value = true;
  clearStatus();
  clearMapObjects();
  currentCategoryLabel.value = contentType;

  try {
    const items = await loadJsonFile(fileName);

    const places = items
      .map((item) => normalizePlace(item, contentType))
      .filter(isValidCoordinate);

    currentPlaces.value = places;
    filteredPlaces.value = [...places];

    await nextTick();
    displayPlaces(filteredPlaces.value);

    showStatus(
      `${contentType} 데이터 ${filteredPlaces.value.length}개를 불러왔습니다.`,
      "success",
    );
  } catch (error) {
    console.error(error);

    currentPlaces.value = [];
    filteredPlaces.value = [];
    displayPlaces([]);

    showStatus(
      `${contentType} 데이터를 불러오지 못했습니다. JSON 파일명과 저장 위치를 확인해주세요.`,
      "error",
    );
  } finally {
    isLoading.value = false;
  }
}

function displayPlaces(places) {
  clearMapObjects(false);

  if (!map || places.length === 0) {
    resetMapPosition();
    return;
  }

  const bounds = new window.kakao.maps.LatLngBounds();

  places.forEach((place, index) => {
    const position = new window.kakao.maps.LatLng(
      place.latitude,
      place.longitude,
    );

    const marker = new window.kakao.maps.Marker({
      map,
      position,
      title: place.title,
    });

    const infoWindow = new window.kakao.maps.InfoWindow({
      content: createInfoWindowContent(place, index),
      removable: true,
    });

    window.kakao.maps.event.addListener(marker, "click", () => {
      closeAllInfoWindows();
      infoWindow.open(map, marker);
      selectPlaceCard(place.id);
    });

    markers.push({
      id: String(place.id),
      marker,
      place,
    });

    infoWindows.push(infoWindow);
    bounds.extend(position);
  });

  if (places.length === 1) {
    map.setCenter(
      new window.kakao.maps.LatLng(
        places[0].latitude,
        places[0].longitude,
      ),
    );
    map.setLevel(5);
    return;
  }

  map.setBounds(bounds, 60, 60, 60, 60);
}

function createInfoWindowContent(place, index) {
  const imageHtml = place.imageUrl
    ? `
      <img
        src="${escapeHtml(place.imageUrl)}"
        alt="${escapeHtml(place.title)}"
        onerror="this.style.display='none'"
      >
    `
    : "";

  return `
    <div class="map-info-window">
      ${imageHtml}
      <strong class="map-info-window-title">
        ${index + 1}. ${escapeHtml(place.title)}
      </strong>
      <p class="map-info-window-address">
        ${escapeHtml(place.address || "주소 정보 없음")}
      </p>
      <span class="map-info-window-category">
        ${escapeHtml(place.contentType)}
      </span>
    </div>
  `;
}

function focusPlace(placeId) {
  const target = markers.find((item) => item.id === String(placeId));

  if (!target || !map) {
    return;
  }

  const { place } = target;

  map.panTo(
    new window.kakao.maps.LatLng(place.latitude, place.longitude),
  );
  map.setLevel(4);

  closeAllInfoWindows();

  const markerIndex = markers.indexOf(target);
  infoWindows[markerIndex]?.open(map, target.marker);

  selectPlaceCard(placeId);
}

async function selectPlaceCard(placeId) {
  selectedPlaceId.value = String(placeId);
  await nextTick();

  placeCardRefs.get(selectedPlaceId.value)?.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
  });
}

function searchPlaces() {
  const keyword = searchKeyword.value.trim().toLowerCase();

  if (!keyword) {
    filteredPlaces.value = [...currentPlaces.value];
    displayPlaces(filteredPlaces.value);
    clearStatus();
    return;
  }

  filteredPlaces.value = currentPlaces.value.filter((place) => {
    const searchableText = [
      place.title,
      place.address,
      place.contentType,
      place.categoryCode,
    ]
      .join(" ")
      .toLowerCase();

    return searchableText.includes(keyword);
  });

  displayPlaces(filteredPlaces.value);

  if (filteredPlaces.value.length === 0) {
    showStatus(
      `"${searchKeyword.value.trim()}"에 해당하는 장소를 찾지 못했습니다.`,
      "warning",
    );
    return;
  }

  showStatus(
    `"${searchKeyword.value.trim()}" 검색 결과 ${filteredPlaces.value.length}개입니다.`,
    "success",
  );
}

function displayRecommendedPlaces(recommendedPlaces) {
  if (!Array.isArray(recommendedPlaces)) {
    return;
  }

  const places = recommendedPlaces
    .map((item) =>
      normalizePlace(
        item,
        item.contentType || item.category || "추천 장소",
      ),
    )
    .filter(isValidCoordinate)
    .sort((a, b) => {
      const orderA = Number.isFinite(a.order) ? a.order : 999;
      const orderB = Number.isFinite(b.order) ? b.order : 999;
      return orderA - orderB;
    });

  currentPlaces.value = places;
  filteredPlaces.value = [...places];
  routePlaces.value = [...places];
  currentCategoryLabel.value = "맞춤 추천";

  displayPlaces(filteredPlaces.value);
  displayRoute(routePlaces.value);
}

function displayRoute(places) {
  clearRoute(false);

  if (!map || places.length < 2) {
    return;
  }

  const path = places.map(
    (place) =>
      new window.kakao.maps.LatLng(place.latitude, place.longitude),
  );

  routePolyline = new window.kakao.maps.Polyline({
    map,
    path,
    strokeWeight: 6,
    strokeColor: "#0f172a",
    strokeOpacity: 0.8,
    strokeStyle: "solid",
  });
}

function clearRoute(clearPlaces = true) {
  if (routePolyline) {
    routePolyline.setMap(null);
    routePolyline = null;
  }

  if (clearPlaces) {
    routePlaces.value = [];
  }
}

function clearMapObjects(clearRouteData = true) {
  markers.forEach((item) => {
    item.marker.setMap(null);
  });

  closeAllInfoWindows();

  markers = [];
  infoWindows = [];
  selectedPlaceId.value = null;

  clearRoute(clearRouteData);
}

function closeAllInfoWindows() {
  infoWindows.forEach((infoWindow) => {
    infoWindow.close();
  });
}

function resetMapPosition() {
  if (!map) {
    return;
  }

  map.setCenter(
    new window.kakao.maps.LatLng(
      DEFAULT_CENTER.latitude,
      DEFAULT_CENTER.longitude,
    ),
  );
  map.setLevel(DEFAULT_LEVEL);
}

function resetMap() {
  searchKeyword.value = "";
  filteredPlaces.value = [...currentPlaces.value];
  displayPlaces(filteredPlaces.value);
  clearStatus();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

onMounted(() => {
  window.displayRecommendedPlaces = displayRecommendedPlaces;
  initializeKakaoMap();
});

onBeforeUnmount(() => {
  clearMapObjects();
  delete window.displayRecommendedPlaces;
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap");

:global(body) {
  margin: 0;
  font-family: "Pretendard", sans-serif;
}

.map-area {
  width: 100%;
  height: 620px;
}

.place-list {
  scrollbar-width: thin;
}

@media (max-width: 1024px) {
  .map-area {
    height: 500px;
  }
}

/*
 * 카카오맵 InfoWindow는 컴포넌트의 scoped 속성 밖에 생성되므로
 * :global()을 사용해야 스타일이 적용된다.
 */
:global(.map-info-window) {
  box-sizing: border-box;
  width: 230px;
  overflow: hidden;
  border-radius: 12px;
  background: white;
  padding: 12px;
  color: #1e293b;
}

:global(.map-info-window img) {
  margin-bottom: 10px;
  height: 110px;
  width: 100%;
  border-radius: 8px;
  object-fit: cover;
}

:global(.map-info-window-title) {
  margin-bottom: 6px;
  display: block;
  font-size: 14px;
  font-weight: 700;
  line-height: 1.4;
}

:global(.map-info-window-address) {
  margin: 0;
  color: #64748b;
  font-size: 12px;
  line-height: 1.4;
}

:global(.map-info-window-category) {
  margin-top: 8px;
  display: inline-block;
  border-radius: 999px;
  background: #f1f5f9;
  padding: 3px 8px;
  color: #475569;
  font-size: 11px;
  font-weight: 600;
}
</style>
