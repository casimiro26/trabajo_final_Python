function chatbotResponse(question) {
    const content = document.getElementById('chatbot-content');
    let response = '';
    switch (question) {
        case '¿Cómo postulo?':
            response = 'Selecciona un área en la página de inicio, sube tu CV en formato PDF o Word, y haz clic en "Enviar a Evaluación".';
            break;
        case '¿Qué archivo debo subir?':
            response = 'Debes subir tu CV en formato PDF o Word (.docx).';
            break;
        case '¿Dónde veo mi resultado?':
            response = 'Después de enviar tu CV, verás tu resultado en la página siguiente. También puedes ver todas las evaluaciones en la sección "Evaluaciones".';
            break;
        case '¿Qué significa observado?':
            response = 'Significa que tu puntaje está entre 50% y 69%. Cumples parcialmente los requisitos, pero puedes mejorar tu presentación.';
            break;
        default:
            response = 'No entendí tu pregunta. Por favor, selecciona una opción.';
    }
    content.innerHTML = `<p><strong>Pregunta:</strong> ${question}</p><p><strong>Respuesta:</strong> ${response}</p>`;
}