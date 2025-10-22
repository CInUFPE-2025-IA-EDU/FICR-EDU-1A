(function(){
  const form = document.getElementById('cadastroForm');
  const msg = document.getElementById('msg');
  form.addEventListener('submit', function(e){
    // Impede envio se houver campo em branco (além do HTML5 required)
    const data = new FormData(form);
    for (const [k,v] of data.entries()){
      if(String(v).trim() === ''){
        e.preventDefault();
        msg.textContent = 'Preencha todos os campos.';
        return;
      }
    }
    // Apenas demonstração:
    e.preventDefault();
    msg.textContent = 'Formulário válido – pronto para enviar!';
  });
})();