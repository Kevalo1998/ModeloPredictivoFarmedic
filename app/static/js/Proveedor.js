$(document).ready(function () {
    var edit = false;
    buscar_prov();
    $('#form-crear').submit(e => {
        let id = $('#id_edit_prov').val();
        let nombre = $('#nombre').val();
        let telefono = $('#telefono').val();
        let correo = $('#correo').val();
        let direccion = $('#direccion').val();
        let url = edit ? '/proveedor/editar' : '/proveedor/crear';

        $.post(url, { id, nombre, telefono, correo, direccion }, (response) => {
            if (response.msg === 'add') {
                $('#add-prov').hide('slow').show(1000).hide(2000);
                $('#form-usuario').trigger('reset');
                buscar_prov();
            } else if (response.msg === 'edit') {
                $('#edit-prove').hide('slow').show(1000).hide(2000);
                $('#form-usuario').trigger('reset');
                buscar_prov();
            } else {
                $('#noadd-prov').hide('slow').show(1000).hide(2000);
                $('#form-usuario').trigger('reset');
            }
            edit = false;
        });
        e.preventDefault();
    });
    function buscar_prov(consulta = '') {
        $.post('/proveedor/buscar', { consulta }, (proveedores) => {
            let template = ``;
            console.log(proveedores);
            proveedores.forEach(p => {
                template += `
                <div provId="${p.id}" provNombre="${p.nombre}" provTelefono="${p.telefono}" provCorreo="${p.correo}" provDireccion="${p.direccion}" provAvatar="${p.avatar}" class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                  <div class="card bg-light d-flex flex-fill">
                    <div class="card-header text-muted border-bottom-0">
                      <h1 class="badge badge-success">Proveedor</h1>
                    </div>
                    <div class="card-body pt-0">
                      <div class="row">
                        <div class="col-7">
                          <h2 class="lead"><b><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">${p.nombre}</font></font></b></h2>
                          <ul class="ml-4 mb-0 fa-ul text-muted">
                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-building"></i></span>Dirección: ${p.direccion}</li>
                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-phone"></i></span>Teléfono: +51 ${p.telefono}</li>
                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-at"></i></span>Correo: ${p.correo}</li>
                          </ul>
                        </div>
                        <div class="col-5 text-center">
                          <img src="${p.avatar}" alt="avatar de proveedor" class="img-circle img-fluid">
                        </div>
                      </div>
                    </div>
                    <div class="card-footer">
                      <div class="text-right">
                        <button class="avatar btn btn-sm btn-info" title="Editar logo" type="button" data-toggle="modal" data-target="#cambiologo">
                          <i class="fas fa-image"></i>
                        </button>
                        <button class="editar btn btn-sm btn-success" title="Editar proveedor" type="button" data-toggle="modal" data-target="#crearproveedor">
                          <i class="fas fa-pencil-alt"></i>
                        </button>
                        <button class="borrar btn btn-sm btn-danger" title="Borrar proveedor">
                          <i class="fas fa-trash-alt"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>`;
            });
            $('#proveedores').html(template);
        });
    }
    $(document).on('keyup', '#buscar_provedor', function () {
        buscar_prov($(this).val());
    });
    $(document).on('click', '.avatar', function () {
        const el = $(this).closest('[provId]');
        $('#logoactual').attr('src', el.attr('provAvatar'));
        $('#nombre_logo').html(el.attr('provNombre'));
        $('#id_logo_prov').val(el.attr('provId'));
        $('#funcion').val('cambiar_logo');  // opcional si lo usas aún
        $('#avatar').val(el.attr('provAvatar'));
    });
    $(document).on('click', '.editar', function () {
        const el = $(this).closest('[provId]');
        $('#id_edit_prov').val(el.attr('provId'));
        $('#nombre').val(el.attr('provNombre'));
        $('#direccion').val(el.attr('provDireccion'));
        $('#telefono').val(el.attr('provTelefono'));
        $('#correo').val(el.attr('provCorreo'));
        edit = true;
    });
    $('#form-logo').submit(e => {
        let formData = new FormData($('#form-logo')[0]);
        $.ajax({
            url: '/proveedor/cambiar_logo',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false
        }).done(function (json) {
            if (json.alert === 'edit') {
                $('#logoactual').attr('src', json.ruta);
                $('#edit-prov').hide('slow').show(1000).hide(2000);
                $('#form-logo').trigger('reset');
                buscar_prov();
            } else {
                $('#noeditip-prov').hide('slow').show(1000).hide(2000);
                $('#form-logo').trigger('reset');
            }
        });
        e.preventDefault();
    });
    $(document).on('click', '.borrar', function () {
        const el = $(this).closest('[provId]');
        const id = el.attr('provId');
        const nombre = el.attr('provNombre');
        const avatar = el.attr('provAvatar');

        Swal.fire({
            title: `Eliminar ${nombre}?`,
            text: 'No se puede recuperar esto',
            imageUrl: avatar,
            showCancelButton: true,
            confirmButtonText: '¡Sí, borrar!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.post('/proveedor/borrar', { id }, (response) => {
                    if (response.msg === 'borrado') {
                        Swal.fire('¡Borrado!', `El proveedor ${nombre} fue borrado.`, 'success');
                        buscar_prov();
                    } else {
                        Swal.fire('No se puede borrar', `El proveedor ${nombre} no puede ser borrado.`, 'error');
                    }
                });
            }
        });
    });
});