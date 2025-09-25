<template>
    <div>
        <h1>Login Administrador</h1>
        <form @submit.prevent = "login">
            <input v-model = "email" type = "email" placeholder = "Email" required />
            <input v-model = "password" type = "password" placeholder = "Contraseña" required />
            <button type = "submit">Ingresar</button>
        </form>
        <p v-if = "mensaje" :class = "['mensaje', 'mensajeTipo']">{{ mensaje }}</p>
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
            mensaje: '',
            mensajeTipo: '',
        }
    },
    methods: {
        async login() {
            try {
                const res = await axios.post('http://localhost:8000/api/admin/login/', {
                    email: this.email,
                    password: this.password
                })
                console.log("Respuesta backend:", res.data)
                this.mensaje = `Bienvenido, ${res.data.nombre || this.email}`;
                this.mensajeTipo = 'success';

                localStorage.setItem('adminToken', res.data.token);

                this.$router.push('/admin/participantes');
            } catch (err) {
                if (err.response) {
                    console.log("Error del backend:", err.response.data)
                    this.mensaje = err.response.data.detail || 'Credenciales inválidas.';
                    this.mensajeTipo = 'error';
                } else if (err.request) {
                    console.log("No hubo respuesta del backend:", err.request)
                    this.mensaje = 'No se pudo conectar con el servidor.'
                    this.mensajeTipo = 'error';
                } else {
                    console.log("Error inesperado:", err.message)
                    this.mensaje = 'Error inesperado.'
                    this.mensajeTipo = 'error';
                }
            }
        }
    }
}
</script>