const botaoAlterarTema = document.getElementById("botao-alterar-tema");  // Criando uma constante para o valor do botao;
const body = document.querySelector("body");  // Criando uma constante para o valor corpo;
const imagemBotaoAlterarTema = document.querySelector(".imagem-botao");  // Criando uma constante para o valor da imagem do botao;


// Criando a funcao que vai no botao de alterar tema;
botaoAlterarTema.addEventListener("click", () => {
    const modoEscuro = body.classList.contains("modo-escuro");  // Verificando se a classe modo escuro esta inserida no body;
    
    body.classList.toggle("modo-escuro");  // Fica alternando entre remover e adicionar a classe ao body;
    
    // Criando a funcao que vai desativar o modo escuro caso ativo;
    if(modoEscuro){
        imagemBotaoAlterarTema.setAttribute("src", "src/imagens/sun.png");  // Alterando a imagem do botao para sol;
    }else{
        imagemBotaoAlterarTema.setAttribute("src", "src/imagens/moon.png");  // ALterando a imagem do botao para lua;
    }
})