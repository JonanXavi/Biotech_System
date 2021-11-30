var compartirModal = document.getElementById('compartir-archivo')
compartirModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreArchivo = button.getAttribute('data-bs-archivo_nombre')

  var modalArchivoC = document.querySelector('#nombreArchivoC')

  modalArchivoC.value = nombreArchivo
});