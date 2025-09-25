<template>
    <div class = "page-container">
        <h1>💘 Inscripción al Sorteo de San Valentín</h1>
        <form @submit.prevent="registrar">
            <input v-model="nombre" type="text" placeholder="Nombre" required />
            <input v-model="email" type="email" placeholder="Email" required />
            <input v-model="telefono" type="text" placeholder="Teléfono" required />
            <button type="submit">💝 Participar</button>
        </form>    
        <p v-if = "mensaje" :class = "['mensaje', 'mensajeTipo']">{{ mensaje }}</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'RegistroForm',
    data() {
        return {
            nombre: '',
            email: '',
            telefono: '',
            mensaje: '',
            mensajeTipo: '',
        }
    },
    methods: {
        async registrar() {
            try {
                await axios.post('http://localhost:8000/api/registro/', {
                    nombre: this.nombre,
                    email: this.email,
                    telefono: this.telefono
                })
                this.mensaje = '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.'
                this.nombre = ''
                this.email = ''
                this.telefono = ''
            } catch (err) {
                if (err.response && err.response.data.email){
                    this.mensaje = err.response.data.email[0]
                } else {
                    this.mensaje = 'Error en el registro.'
                }
            }
        }
    }
}
</script>