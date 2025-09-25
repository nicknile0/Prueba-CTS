<template>
    <div>
        <h1>Lista de Participantes</h1>

        <input 
            v-model="filtro" 
            type="text" 
            placeholder="Buscar por nombre o correo..."
            class="search-bar"
        />

        <ul class = "participantes-lista">
            <li v-for = "p in participantesFiltrados" :key = "p.id" class = "participante-item">
                {{ p.nombre }} - {{ p.email }} -
                <span :style="{color: p.verificado ? '#28a745' : '#dc3545'}">
                    {{ p.verificado ? 'Verificado' : 'No Verificado' }}
                </span>
            </li>
        </ul>
        <button @click="$router.push('/admin/sorteo')">Ir al Sorteo</button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'PanelParticipantes',
    data() {
        return {
            participantes: [],
            filtro: ''
        }
    },
    computed: {
        participantesFiltrados() {
            return this.participantes.filter(p =>
                p.nombre.toLowerCase().includes(this.filtro.toLowerCase()) ||
                p.email.toLowerCase().includes(this.filtro.toLowerCase())
            )
        }
    },
    async mounted() {
        try {
            const token = localStorage.getItem('adminToken');
            const res = await axios.get('http://localhost:8000/api/admin/participantes/', {
                headers: { Authorization: `Token ${token}` }
            })
            this.participantes = Array.isArray(res.data) ? res.data : res.data.results
        } catch (err) {
            console.error('Error al cargar participantes', err)
        }
    }
}
</script>