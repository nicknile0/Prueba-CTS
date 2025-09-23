<template>
    <div>
        <h1>Sorteo del Ganador</h1>
        <button @click = "elegirGanador">Elegir Ganador</button>
        <p v-if = "ganador">
            Ganador: {{ ganador.nombre }} - {{ ganador.email }}
        </p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'PanelSorteo',
    data() {
        return {
            ganador: null
        }
    },
    methods: {
        async elegirGanador() {
            try {
                const res = await axios.post('http://localhost:8000/api/admin/sorteo/', {})
                this.ganador = {
                    nombre: res.data.nombre,
                    email: res.data.email
                }
            } catch (err) {
                console.error('Error al elegir ganador', err)
            }
        }
    }
}
</script>