import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import BoardView from '../views/BoardView.vue'
import FavoriteView from '../views/FavoriteView.vue'
import MapView from '../views/MapView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/board',
      name: 'board',
      component: BoardView,
    },
    {
      path: '/favorite',
      name: 'favorite',
      component: FavoriteView,
    },
    {
      path: '/map',
      name: 'map',
      component: MapView,
    },
    {
      path: '/board/write',
      name: 'board-write',
      component: () => import('../views/BoardWriteView.vue'),
    },
    {
      path: "/board/edit/:id",
      name: "board-edit",
      component: () => import("../views/BoardEditView.vue")
    },

  ],
})

export default router