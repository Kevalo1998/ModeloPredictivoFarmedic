$(document).ready(function() {
    var funcion; 
    var edit = false; 
    buscar_lab();

    $('#form-crear-laboratorio').submit(e => {
        let nombre_laboratorio = $('#nombre-laboratorio').val();
        let id_editado = $('#id_editar_lab').val();
        let ruta = edit ? '/laboratorio/editar' : '/laboratorio/crear';

        $.post(ruta, { nombre_laboratorio, id_editado }, (response) => {
            if (response.msg === 'add') {
                $('#add-laboratorio').hide('slow').show(1000).hide(2000);
            } else if (response.msg === 'noadd') {
                $('#noadd-laboratorio').hide('slow').show(1000).hide(2000);
            } else if (response.msg === 'edit') {
                $('#edit-lab').hide('slow').show(1000).hide(2000);
            }
            $('#form-crear-laboratorio').trigger('reset');
            buscar_lab();
            edit = false;
        });
        e.preventDefault();
    });
    function buscar_lab(consulta = '') {
        $.post('/laboratorio/buscar', { consulta }, (laboratorios) => {
            let template = '';
            console.log(laboratorios);
            laboratorios.forEach(laboratorio => {
                template += `
                <tr labId="${laboratorio.id}" labNombre="${laboratorio.nombre}" labAvatar="${laboratorio.avatar}">
                    <td>
                        <button class="avatar btn btn-info" title="Cambiar logo de laboratorio" type="button" data-toggle="modal" data-target="#cambiologo">
                            <i class="far fa-image"></i>
                        </button>
                        <button class="editar btn btn-success" title="Editar laboratorio" type="button" data-toggle="modal" data-target="#crearlaboratorio">
                            <i class="fas fa-pencil-alt"></i>
                        </button>
                        <button class="borrar btn btn-danger" title="Borrar laboratorio">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>   
                    <td>
                        <img src="${laboratorio.avatar}" class="img-fluid rounded" width="70" height="70">
                    </td>
                    <td>${laboratorio.nombre}</td>
                </tr>`;
            });
            $('#laboratorios').html(template);
        });
    }
    $(document).on('keyup', '#buscar-laboratorio', function() {
        buscar_lab($(this).val());
    });
    $(document).on('click', '.avatar', (e) => {
        const el = $(e.currentTarget).closest('[labId]');
        $('#logoactual').attr('src', el.attr('labAvatar'));
        $('#nombre_logo').html(el.attr('labNombre'));
        $('#funcion').val('cambiar_logo');
        $('#id_logo_lab').val(el.attr('labId'));
    });
    $('#form-logo').submit(e => {    
        let formData = new FormData($('#form-logo')[0]);
        $.ajax({
            url: '/laboratorio/cambiar_logo',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false
        }).done(function(json) {
            if (json.alert == 'edit') { 
                $('#logoactual').attr('src', json.ruta);
                $('#form-logo').trigger('reset');
                $('#edit').hide('slow').show(1000).hide(2000);
                buscar_lab();
            } else {
                $('#noedit').hide('slow').show(1000).hide(2000);
                $('#form-logo').trigger('reset');
            }
        });
        e.preventDefault();
    });
    $(document).on('click', '.borrar', (e) => {
        const el = $(e.currentTarget).closest('[labId]');
        const id = el.attr('labId');
        const nombre = el.attr('labNombre');
        const avatar = el.attr('labAvatar');

        Swal.fire({
            title: 'Eliminar ' + nombre + '?',
            text: 'No se puede recuperar esto',
            imageUrl: avatar,
            showCancelButton: true,
            confirmButtonText: '¡Sí, borrar!',
            cancelButtonText: 'No, Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.post('/laboratorio/borrar', { id }, (response) => {
                    if (response.msg == 'borrado') {
                        Swal.fire('¡Borrado!', 'El laboratorio ' + nombre + ' fue borrado', 'success');
                        buscar_lab();
                    } else {
                        Swal.fire('No se puede borrar', 'El laboratorio ' + nombre + ' tiene productos asociados', 'error');
                    }
                });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                Swal.fire('Cancelado', 'El laboratorio ' + nombre + ' no fue borrado', 'error');
            }
        });
    });
    $(document).on('click', '.editar', (e) => {
        const el = $(e.currentTarget).closest('[labId]');
        $('#id_editar_lab').val(el.attr('labId'));
        $('#nombre-laboratorio').val(el.attr('labNombre'));
        edit = true;
    });
    
});