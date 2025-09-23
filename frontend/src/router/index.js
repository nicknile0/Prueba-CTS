import { createRouter, createWebHistory } from "vue-router";
import RegistroForm from "../views/RegistroForm.vue";
import VerificacionForm from "../views/VerificacionForm.vue";
import LoginAdmin from "../views/LoginAdmin.vue";
import PanelParticipantes from "../views/PanelParticipantes.vue";
import PanelSorteo from "../views/PanelSorteo.vue";

const routes = [
  { path: "/", component: RegistroForm },
  { path: "/verificar", component: VerificacionForm },
  { path: "/admin/login", component: LoginAdmin },
  { path: "/admin/participantes", component: PanelParticipantes },
  { path: "/admin/sorteo", component: PanelSorteo },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
