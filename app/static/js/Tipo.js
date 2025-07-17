$(document).ready(function() {
    buscar_tip();
    var edit = false; 
    $('#form-crear-tipo').submit(e => {
        let nombre_tipo = $('#nombre-tipo').val();
        let id_editado = $('#id_editar_tip').val();
        let url = edit ? '/tipo/editar' : '/tipo/crear';

        $.post(url, { nombre_tipo, id_editado }, (response) => {
            if (response.msg == 'add') {
                $('#add-tipo').hide('slow').show(1000).hide(2000);
                $('#form-crear-tipo').trigger('reset');
                buscar_tip();
            } else if (response.msg == 'noadd') {
                $('#noadd-tipo').hide('slow').show(1000).hide(2000);
                $('#form-crear-tipo').trigger('reset');
            } else if (response.msg == 'edit') {
                $('#edit-tip').hide('slow').show(1000).hide(2000);
                $('#form-crear-tipo').trigger('reset');
                buscar_tip();
            }
            edit = false;
        });
        e.preventDefault();
    });
    function buscar_tip(consulta = '') {
        $.post('/tipo/buscar', { consulta }, (response) => {
            let template = '';
            response.forEach(tipo => {
                template += `
                    <tr tipId="${tipo.id}" tipNombre="${tipo.nombre}">
                        <td>
                            <button class="editar-tip btn btn-success" title="Editar tipo" type="button" data-toggle="modal" data-target="#creartipo">
                                <i class="fas fa-pencil-alt"></i>
                            </button>
                            <button class="borrar-tip btn btn-danger" title="Borrar tipo">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </td>
                        <td>${tipo.nombre}</td>
                    </tr>`;
            });
            $('#tipos').html(template);
        });
    }
    $(document).on('keyup', '#buscar-tipo', function() {
        let valor = $(this).val();
        buscar_tip(valor);
    });
    $(document).on('click', '.borrar-tip', function() {
        const elemento = $(this).closest('tr');
        const id = $(elemento).attr('tipId');
        const nombre = $(elemento).attr('tipNombre');

        Swal.fire({
            title: `Eliminar ${nombre}?`,
            text: 'No se puede recuperar esto',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: '¡Sí, borralo!',
            cancelButtonText: 'No, cancelar',
            reverseButtons: true
        }).then(result => {
            if (result.isConfirmed) {
                $.post('/tipo/borrar', { id }, (response) => {
                    if (response.msg == 'borrado') {
                        Swal.fire('Borrado!', `El tipo ${nombre} fue borrado.`, 'success');
                        buscar_tip();
                    } else {
                        Swal.fire('No se puede borrar!', `El tipo ${nombre} no puede ser borrado, hay productos con este tipo.`, 'error');
                    }
                });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                Swal.fire('Cancelado', `El tipo ${nombre} no fue borrado`, 'error');
            }
        });
    });
    $(document).on('click', '.editar-tip', function() {
        const elemento = $(this).closest('tr');
        const id = $(elemento).attr('tipId');
        const nombre = $(elemento).attr('tipNombre');
        $('#id_editar_tip').val(id);
        $('#nombre-tipo').val(nombre);
        edit = true;
    });
});