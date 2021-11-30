var archivoModal = document.getElementById('archivo-editar')
archivoModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget
  var nombreArchivo = button.getAttribute('data-bs-archivo_nombre')
  var descripcionArchivo = button.getAttribute('data-bs-archivo_desc')
  var DescargasArchivo = button.getAttribute('data-bs-num_descargas')
  var publicable = button.getAttribute('data-bs-archivo_pub')
  var descargar = button.getAttribute('data-bs-archivo_descarga')

  var modalArchivo = document.querySelector('#nombreArchivo')
  var modalDescArchivo = document.querySelector('#descripcion-archivo')
  var modalDescargas = document.querySelector('#descargas')
  var modalPublicable = document.querySelector('#publicable')
  var modalDescarga = document.querySelector('#op-descarga')

  modalArchivo.value = nombreArchivo
  modalDescArchivo.value = descripcionArchivo
  modalDescargas.value = DescargasArchivo

  if(publicable === 'S'){
    modalPublicable.checked=true
  }
  else if(publicable === 'N'){
    modalPublicable.checked=false
  }

  if(descargar === 'S'){
    modalDescarga.checked=true
  }
  else if(descargar === 'N'){
    modalDescarga.checked=false
  }
});