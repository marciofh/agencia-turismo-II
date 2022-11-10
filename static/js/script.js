// Selecionar datas a partir do dia atual.    
$(function(){
  var dtToday = new Date();
  
  var mes = dtToday.getMonth() + 1;
  var dia= dtToday.getDate();
  var ano = dtToday.getFullYear();
  if(mes < 10)
      mes = '0' + mes.toString();
  if(dia < 10)
      dia = '0' +dia.toString();
  
  var maxDate = ano + '-' + mes + '-' + dia;
  
  $('#dataida').attr('min', maxDate);
  $('#datavolta').attr('min', maxDate);
});

// Validação de campos digitados iguais
function validar(){
  var origin = document.getElementById('origin');
  var destination = document.getElementById('destination');
  var button = document.getElementById('sendButton');

  if (origin.value == destination.value){
      alert("As cidades de origem e destino tem que ser diferentes!");
      button.disabled = true;
  } else {
      button.disabled = false;
      }
  }

// Input
  
let timer;

document.addEventListener('input', e => {
const el = e.target;

if( el.matches('[data-color]') ) {
  clearTimeout(timer);
  timer = setTimeout(() => {
    document.documentElement.style.setProperty(`--color-${el.dataset.color}`, el.value);
  }, 100)
}
})