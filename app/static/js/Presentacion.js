$(document).ready(function () {
    buscar_pre();
    var edit = false;

    $('#form-crear-presentacion').submit(e => {
        e.preventDefault();
        let nombre_presentacion = $('#nombre-presentacion').val();
        let id_editado = $('#id_editar_pre').val();
        let url = edit ? '/presentacion/editar' : '/presentacion/crear';

        $.post(url, {
            nombre_presentacion: nombre_presentacion,
            id_editado: id_editado
        }, response => {
            if (response === 'add') {
                $('#add-pre').hide('slow').show(1000).hide(2000);
                $('#form-crear-presentacion').trigger('reset');
                buscar_pre();
            } else if (response === 'noadd') {
                $('#noadd-pre').hide('slow').show(1000).hide(2000);
                $('#form-crear-presentacion').trigger('reset');
            } else if (response === 'edit') {
                $('#edit-pre').hide('slow').show(1000).hide(2000);
                $('#form-crear-presentacion').trigger('reset');
                buscar_pre();
            }
            edit = false;
        });
    });

    function buscar_pre(consulta = '') {
        $.post('/presentacion/buscar', { consulta }, response => {
            let template = '';
            response.forEach(presentacion => {
                template += `
                <tr preId="${presentacion.id}" preNombre="${presentacion.nombre}">
                    <td>
                        <button class="editar-pre btn btn-success" title="Editar presentación" type="button" data-toggle="modal" data-target="#crearpresentacion">
                            <i class="fas fa-pencil-alt"></i>
                        </button>
                        <button class="borrar-pre btn btn-danger" title="Borrar presentación">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                    <td>${presentacion.nombre}</td>
                </tr>`;
            });
            $('#presentaciones').html(template);
        });
    }

    $(document).on('keyup', '#buscar-presentacion', function () {
        let valor = $(this).val();
        buscar_pre(valor);
    });

    $(document).on('click', '.borrar-pre', function () {
        const elemento = $(this).closest('tr');
        const id = $(elemento).attr('preId');
        const nombre = $(elemento).attr('preNombre');

        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: "btn btn-success",
                cancelButton: "btn btn-danger mr-1"
            },
            buttonsStyling: false
        });

        swalWithBootstrapButtons.fire({
            title: '¿Eliminar ' + nombre + '?',
            text: 'No se puede recuperar esto',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: '¡Sí, bórralo!',
            cancelButtonText: 'No, cancelar',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                $.post('/presentacion/borrar', { id }, response => {
                    if (response === 'borrado') {
                        swalWithBootstrapButtons.fire('¡Borrado!', 'La presentación ' + nombre + ' fue eliminada.', 'success');
                        buscar_pre();
                    } else {
                        swalWithBootstrapButtons.fire('¡Error!', 'No se puede borrar la presentación ' + nombre + ', hay productos asociados.', 'error');
                    }
                });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                swalWithBootstrapButtons.fire('Cancelado', 'La presentación ' + nombre + ' no fue eliminada.', 'error');
            }
        });
    });

    $(document).on('click', '.editar-pre', function () {
        const elemento = $(this).closest('tr');
        const id = $(elemento).attr('preId');
        const nombre = $(elemento).attr('preNombre');
        $('#id_editar_pre').val(id);
        $('#nombre-presentacion').val(nombre);
        edit = true;
    });
});