<template>
    <div>
        <h1>Sorteo del Ganador</h1>
        <div v-if="ganador" class="ganador-box">
        🎉 Ganador: <strong>{{ ganador.nombre }}</strong> - {{ ganador.email }}
        </div>

        <button class="primary-btn" @click="elegirGanador">Elegir Ganador</button>

        <button class="secondary-btn" @click="$router.push('/admin/participantes')">
        Volver a participantes
        </button>
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
                const token = localStorage.getItem('adminToken');
                const res = await axios.post('http://localhost:8000/api/admin/sorteo/', {},
                    {
                        headers: { Authorization: `Token ${token}` }
                    }
                )
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