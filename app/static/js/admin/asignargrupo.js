var newfolderModal = document.getElementById('asignar-grupo')
newfolderModal.addEventListener('show.bs.modal', function (event) {

  var button = event.relatedTarget

  var nombreInvestigador = button.getAttribute('data-bs-investigador-nombre')
  var idtUsuario = button.getAttribute('data-bs-usuario-idt')
  var userInvest = button.getAttribute('data-bs-user-invest')

  var modalnombreUser = document.querySelector('#nombreInvestigador')
  var modaluserID = document.querySelector('#usuarioID')
  var modaluserInvest= document.querySelector('#userInvest')

  modalnombreUser.value = nombreInvestigador
  modaluserID.value = idtUsuario
  modaluserInvest.value = userInvest
});