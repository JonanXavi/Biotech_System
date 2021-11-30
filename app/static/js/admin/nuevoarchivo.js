var newfileModal = document.getElementById('subir-archivo')
newfileModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreArchivo = button.getAttribute('data-bs-new-file')

  var modalnewFile = document.querySelector('#newFile')

  modalnewFile.value = nombreArchivo
});