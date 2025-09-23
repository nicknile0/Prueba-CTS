<template>
    <div>
        <h1>Registro para el sorteo</h1>
        <form @submit.prevent = "registrar">
            <input v-model = "nombre" placeholder = "Nombre completo" required />
            <input v-model = "email" type = "email" placeholder = "Correo electrónico" required />
            <input v-model = "telefono" placeholder = "Teléfono" required />
            <button type = "submit">Registrarse</button>
        </form>    
        <p v-if = "mensaje">{{ mensaje }}</p>
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
            mensaje: ''
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