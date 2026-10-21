const API = 'http://127.0.0.1:8000';

const formLogin = document.getElementById('form-login');

formLogin.addEventListener('submit', async (e) => {
e.preventDefault();

// Remove o token antigo antes de tentar entrar novamente.
localStorage.removeItem('token');

const dados = {
    email: document.getElementById('email').value,
    senha: document.getElementById('senha').value
};

try {
    const resposta = await fetch(`${API}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();

    // Só permite entrar se o backend retornar um token.
    if (resposta.ok && resultado.access_token) {
        localStorage.setItem('token', resultado.access_token);
        window.location.href = 'dashboard.html';
    } else {
        alert(
            'Erro ao entrar: ' +
            (resultado.detail || resultado.erro || 'E-mail ou senha inválidos.')
        );
    }
} catch (erro) {
    alert('Não foi possível conectar ao servidor.');
    console.error('Erro no login:', erro);
}

});