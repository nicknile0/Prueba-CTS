<template>
    <div>
        <h1>Lista de Participantes</h1>
        <ul>
            <li v-for = "p in participantes" :key = "p.id">
                {{ p.nombre }} - {{ p.email }} - {{ p.verificado ? 'Verificado' : 'No Verificado' }}
            </li>
        </ul>
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
            const res = await axios.get('http://localhost:8000/api/admin/participantes/', {

            })
            this.participantes = res.data
        } catch (err) {
            console.error('Error al cargar participantes', err)
        }
    }
}
</script>