<template>
    <div>
        <h1>Login Administrador</h1>
        <form @submit.prevent = "login">
            <input v-model = "email" type = "email" placeholder = "Email" required />
            <input v-model = "password" type = "password" placeholder = "Contraseña" required />
            <button type = "submit">Ingresar</button>
        </form>
        <p v-if = "mensaje">{{ mensaje }}</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'LoginAdmin',
    data() {
        return {
            email: '',
            password: '',
            mensaje: ''
        }
    },
    methods: {
        async login() {
            try {
                await axios.post('http://localhost:8000/api/admin/login/', {
                    email: this.email,
                    password: this.password
                })
                this.mensaje = 'Bienvenido, ${res.data.nombre || this.email}'
                this.email = ''
                this.password = ''
            } catch (err) {
                this.mensaje = 'Credenciales inválidas.'
            }
        }
    }
}
</script>