let timer;
const inactivityTime = 20000; // 1 minuto en milisegundos (60000 ms)
const redirectUrl = "/otra-vista/"; // Cambia esto por la URL de la vista de destino
console.log("inact staticfiles")
// Función para reiniciar el temporizador
function resetTimer() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        window.location.href = redirectUrl; // Redirige a otra vista después del tiempo de inactividad
    }, inactivityTime);
}

// Detectar actividad del usuario (movimiento del ratón o clic)
document.addEventListener('mousemove', resetTimer);  // Detecta el movimiento del ratón
document.addEventListener('click', resetTimer);      // Detecta clics
document.addEventListener('keydown', resetTimer);    // Detecta teclas presionadas

// Inicializar el temporizador
resetTimer();
