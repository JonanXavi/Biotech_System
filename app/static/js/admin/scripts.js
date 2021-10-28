/*!
    * Start Bootstrap - SB Admin v7.0.2 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2021 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function mostrarPassword(){
		var cambio = document.getElementById("password");
		if(cambio.type == "password"){
			cambio.type = "text";
			$('.icon').removeClass('fa fa-eye-slash').addClass('fa fa-eye');
		}else{
			cambio.type = "password";
			$('.icon').removeClass('fa fa-eye').addClass('fa fa-eye-slash');
		}
	} 
	
	$(document).ready(function () {
	$('#ShowPassword').click(function () {
		$('#Password').attr('type', $(this).is(':checked') ? 'text' : 'password');
	});
});

var carpetaModal = document.getElementById('carpeta-editar')
carpetaModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreCarpeta = button.getAttribute('data-bs-carpeta_nombre')
  var grupoCarperta = button.getAttribute('data-bs-carpeta_grupo')
  var descripcionCarpeta = button.getAttribute('data-bs-carpeta_desc')
  var Privado = button.getAttribute('data-bs-carpeta_priv')

  var modalTitulo = document.querySelector('.modal-title')
  var modalGrupo = document.querySelector('#grupo')
  var modalBodyInput = document.querySelector('#descripcion-carpeta')
  var modalBodyInput1 = document.querySelector('#opcion')

  modalTitulo.textContent = nombreCarpeta
  modalGrupo.value = grupoCarperta
  modalBodyInput.value = descripcionCarpeta

  if(Privado === 'S'){
    modalBodyInput1.checked=true
  }
  else if(Privado === 'N'){
    modalBodyInput1.checked=false
  }
});