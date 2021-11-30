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

function noEspacios(){
    var er = new RegExp(/\s/);
    var web = document.getElementById('carpetaNueva').value;
    if(er.test(web)){
        alert('El nombre no puede tener espacios en blanco');
        return false;
    }
    else
        return true;
}

function habilitarBoton(){
    pass1 = document.getElementById('contrasena');
    pass2 = document.getElementById('contrasena2');
    boton = document.getElementById("create");

    if (pass1.value !== pass2.value) {
        document.getElementById("error").classList.remove("ocultar");
        document.getElementById("ok").classList.remove("mostrar");
        document.getElementById("error").classList.add("mostrar");
        document.getElementById("ok").classList.add("ocultar");
        boton.disabled = true;
    } else {
        document.getElementById("error").classList.add("ocultar");
        document.getElementById("ok").classList.remove("ocultar");
        document.getElementById("error").classList.remove("mostrar");
        document.getElementById("ok").classList.add("mostrar");
        boton.disabled = false;
    }
}

function cargaArchivo(){
    document.getElementById("uploadGif").style.display='block';
    document.getElementById("uploadBtn").disabled=true;
    return true;
}