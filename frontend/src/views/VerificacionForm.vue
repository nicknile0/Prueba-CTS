<template>
    <div>
        <h1>Verificación y creación de contraseña</h1>
        <form @submit.prevent = "verificar">
            <input v-model = "password" type = "password" placeholder = "Contraseña" required />
            <input v-model = "password2" type = "password" placeholder = "Repite la contraseña" required />
            <button type = "submit">Activar cuenta</button>
        </form>
        <p v-if = "mensaje">{{ mensaje }}</p>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name : 'VerificacionForm',
    data() {
        return {
            password: '',
            password2: '',
            mensaje: '',
            token: '',
            verificado: false,
        }
    },
    mounted() {
        const urlParams = new URLSearchParams(window.location.search);
        this.token = urlParams.get('token');
        if (!this.token) {
            this.mensaje = 'Token no encontrado en la URL.';
        }
    },
    methods: {
        async verificar() {
            if (this.password !== this.password2) {
                this.mensaje = 'Las contraseñas no coinciden.'
                return
            }
            try {
                await axios.post('http://localhost:8000/api/verificar/', {
                    token: this.token,
                    password: this.password
                })
                this.mensaje = 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.'
                this.token = ''
                this.password = ''
                this.password2 = ''
                this.verificado = true
            } catch (err) {
                if (err.response && err.response.data.detail) {
                    this.mensaje = err.response.data.detail
                } else {
                    this.mensaje = 'Error en la verificación.'
                }
            }
        }
    }
}
</script>