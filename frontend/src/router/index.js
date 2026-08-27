import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue'
import OrganizationsView from '@/views/OrganizationsView.vue'
import ClubsView from '@/views/ClubsView.vue'
import TeamsView from '@/views/TeamsView.vue'
import PlayersView from '@/views/PlayersView.vue'
import MatchesView from '@/views/MatchesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/organizations',
      name: 'organizations',
      component: OrganizationsView,
    },
    {
      path: '/clubs',
      name: 'clubs',
      component: ClubsView,
    },
    {
      path: '/teams',
      name: 'teams',
      component: TeamsView,
    },
    {
      path: '/players',
      name: 'players',
      component: PlayersView,
    },
    {
      path: '/matches',
      name: 'matches',
      component: MatchesView,
    },
    {
      path: '/matches/:matchId',
      name: 'match-details',
      component: () => import('@/views/MatchDetailsView.vue')
    },
  ],
})

export default router
