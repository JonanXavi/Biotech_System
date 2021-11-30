var newfolderModal = document.getElementById('nueva-carpeta')
newfolderModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreCarpeta = button.getAttribute('data-bs-new-nombre')

  var modalnewFolder = document.querySelector('#newFolder')

  modalnewFolder.value = nombreCarpeta
});