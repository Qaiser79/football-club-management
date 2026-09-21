import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '@/views/DashboardView.vue'
import OrganizationsView from '@/views/OrganizationsView.vue'
import ClubsView from '@/views/ClubsView.vue'
import TeamsView from '@/views/TeamsView.vue'
import PlayersView from '@/views/PlayersView.vue'
import MatchesView from '@/views/MatchesView.vue'
import MatchDetailsView from '@/views/MatchDetailsView.vue'
import CoachesView from '@/views/CoachesView.vue'
import ManagersView from '@/views/ManagersView.vue'


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
      path: '/players/:playerId',
      name: 'player-details',
      component: () => import ('@/views/PlayerDetailsView.vue'),
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


    {
      path: '/coaches',
      name: 'coaches',
      component: CoachesView
    },

    {
      path: '/coaches/:coachId', 
      name: 'coach-details',
      component: ()=> import('@/views/CoachDetailsView.vue')
    },

    {
      path: '/managers',
      name: 'managers',
      component: ManagersView,
    },

    {
      path: '/managers/:managerId',
      name: 'manager-details',
      component: () => import('@/views/ManagerDetailsView.vue'),
    },
  ],
})

export default router
