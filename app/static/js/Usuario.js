$(document).ready(function () {
    let edit = false;
    const id_usuario = $('#id_usuario').val();

    buscar_usuario(id_usuario);

    function buscar_usuario(dato) {
        $.post('/usuario/buscar', { dato }, (response) => {
            const usuario = response;
            $('#nombre_us').html(usuario.nombre);
            $('#apellidos_us').html(usuario.apellidos);
            $('#edad').html(usuario.edad);
            $('#dni_us').html(usuario.dni);

            let tipo = '';
            switch (usuario.tipo) {
                case 'Propietario':
                    tipo = `<h1 class="badge badge-danger">${usuario.tipo}</h1>`;
                    break;
                case 'Administrador':
                    tipo = `<h1 class="badge badge-warning">${usuario.tipo}</h1>`;
                    break;
                case 'Quimico':
                    tipo = `<h1 class="badge badge-info">${usuario.tipo}</h1>`;
                    break;
                case 'Tecnico':
                    tipo = `<h1 class="badge badge-primary">${usuario.tipo}</h1>`;
                    break;
            }
            $('#us_tipo').html(tipo);
            $('#telefono_us').html(usuario.telefono);
            $('#residencia_us').html(usuario.residencia);
            $('#correo_us').html(usuario.correo);
            $('#sexo_us').html(usuario.sexo);
            $('#adicional_us').html(usuario.adicional);

            $('#avatar').attr('src', usuario.avatar);
        });
    }
    $(document).on('click', '.edit', (e) => {
        edit = true;
        $.post('/usuario/capturar', { id_usuario }, (response) => {
            const usuario = response;
            $('#telefono').val(usuario.telefono);
            $('#residencia').val(usuario.residencia);
            $('#correo').val(usuario.correo);
            $('#sexo').val(usuario.sexo);
            $('#adicional').val(usuario.adicional);
        });
    });
    $('#form-usuario').submit((e) => {
        e.preventDefault();
        if (edit) {
            const data = {
                id_usuario,
                telefono: $('#telefono').val(),
                residencia: $('#residencia').val(),
                correo: $('#correo').val(),
                sexo: $('#sexo').val(),
                adicional: $('#adicional').val()
            };
            $.post('/usuario/editar', data, (response) => {
                if (response === 'editado') {
                    $('#editado').fadeIn().delay(2000).fadeOut();
                    $('#form-usuario').trigger('reset');
                    buscar_usuario(id_usuario);
                }
                edit = false;
            });
        } else {
            $('#noeditado').fadeIn().delay(2000).fadeOut();
            $('#form-usuario').trigger('reset');
        }
    });
    $('#form-pass').submit((e) => {
        e.preventDefault();
        const data = {
            id_usuario,
            oldpass: $('#oldpass').val(),
            newpass: $('#newpass').val()
        };
        $.post('/usuario/cambiar_contra', data, (response) => {
            if (response === 'update') {
                $('#update').fadeIn().delay(2000).fadeOut();
            } else {
                $('#noupdate').fadeIn().delay(2000).fadeOut();
            }
            $('#form-pass').trigger('reset');
        });
    });

    $('#form-photo').submit((e) => {
        e.preventDefault();
        const formData = new FormData($('#form-photo')[0]);
        $.ajax({
            url: '/usuario/cambiar_foto',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false
        }).done((json) => {
            if (json.alert === 'edit') {
                $('#avatar').attr('src', json.ruta);
                $('#edit').fadeIn().delay(2000).fadeOut();
                $('#form-photo').trigger('reset');
                buscar_usuario(id_usuario);
            } else {
                $('#noedit').fadeIn().delay(2000).fadeOut();
                $('#form-photo').trigger('reset');
            }
        });
    });
});