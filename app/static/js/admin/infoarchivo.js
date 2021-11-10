var compartirModal = document.getElementById('compartir-archivo')
compartirModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreArchivoC = button.getAttribute('data-bs-archivo_nombreC')

  var modalArchivoC = document.querySelector('#nombreArchivoC')

  modalArchivoC.value = nombreArchivoC
});