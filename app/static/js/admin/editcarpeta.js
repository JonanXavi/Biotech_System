var carpetaModal = document.getElementById('carpeta-editar')
carpetaModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreCarpeta = button.getAttribute('data-bs-carpeta_nombre')
  var grupoCarperta = button.getAttribute('data-bs-carpeta_grupo')
  var descripcionCarpeta = button.getAttribute('data-bs-carpeta_desc')
  var Privado = button.getAttribute('data-bs-carpeta_priv')

  var modalCarpeta = document.querySelector('#nombreCarpeta')
  var modalGrupo = document.querySelector('#grupo')
  var modalBodyInput = document.querySelector('#descripcion-carpeta')
  var modalBodyInput1 = document.querySelector('#opcion')

  modalCarpeta.value = nombreCarpeta
  modalGrupo.value = grupoCarperta
  modalBodyInput.value = descripcionCarpeta

  if(Privado === 'S'){
    modalBodyInput1.checked=true
  }
  else if(Privado === 'N'){
    modalBodyInput1.checked=false
  }
});