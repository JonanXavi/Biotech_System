var archivoModal = document.getElementById('archivo-editar')
archivoModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreArchivo = button.getAttribute('data-bs-archivo_nombre')
  var carpetaArchivo = button.getAttribute('data-bs-archivo_carpeta')
  var descripcionArchivo = button.getAttribute('data-bs-archivo_desc')
  var DescargasArchivo = button.getAttribute('data-bs-num_descargas')
  var publicable = button.getAttribute('data-bs-archivo_pub')
  var compartir = button.getAttribute('data-bs-archivo_comp')
  var descargar = button.getAttribute('data-bs-archivo_descarga')

  var modalTituloArch = document.querySelector('.modal-title')
  var modalArchivo = document.querySelector('#nombreArchivo')
  var modalCarpeta = document.querySelector('#carpeta')
  var modalDescArchivo = document.querySelector('#descripcion-archivo')
  var modalDescargas = document.querySelector('#descargas')
  var modalPublicable = document.querySelector('#publicable')
  var modalCompartir = document.querySelector('#compartir')
  var modalDescarga = document.querySelector('#op-descarga')

  modalTituloArch.textContent = nombreArchivo
  modalArchivo.value = nombreArchivo
  modalCarpeta.value = carpetaArchivo
  modalDescArchivo.value = descripcionArchivo
  modalDescargas.value = DescargasArchivo

  if(publicable === 'S'){
    modalPublicable.checked=true
  }
  else if(publicable === 'N'){
    modalPublicable.checked=false
  }

  if(compartir === 'S'){
    modalCompartir.checked=true
  }
  else if(compartir === 'N'){
    modalCompartir.checked=false
  }

  if(descargar === 'S'){
    modalDescarga.checked=true
  }
  else if(descargar === 'N'){
    modalDescarga.checked=false
  }
});