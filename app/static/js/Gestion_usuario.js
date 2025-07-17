$(document).ready(function () {
    var tipo_usuario = $('#tipo_usuario').val();
    buscar_datos();
    if (tipo_usuario == 3 || tipo_usuario == 4) {
        $('#button-crear').hide();
    }

    function buscar_datos(consulta = '') {
        $.post('/usuario/listar', { consulta }, (usuarios) => {
            let template = '';
            usuarios.forEach(usuario => {
                template += `
                    <div usuarioId="${usuario.id}" class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                        <div class="card bg-light d-flex flex-fill">
                            <div class="card-header text-muted border-bottom-0">`;

                if (usuario.tipo_usuario == 1) {
                    template += `<h1 class="badge badge-danger">${usuario.tipo}</h1>`;
                }
                if (usuario.tipo_usuario == 2) {
                    template += `<h1 class="badge badge-warning">${usuario.tipo}</h1>`;
                }
                if (usuario.tipo_usuario == 3) {
                    template += `<h1 class="badge badge-info">${usuario.tipo}</h1>`;
                }
                if (usuario.tipo_usuario == 4) {
                    template += `<h1 class="badge badge-primary">${usuario.tipo}</h1>`;
                }

                template += `</div>
                            <div class="card-body pt-0">
                                <div class="row">
                                    <div class="col-7">
                                        <h2 class="lead"><b>${usuario.nombre} ${usuario.apellidos}</b></h2>
                                        <p class="text-muted text-sm"><b>Acerca de:</b> ${usuario.adicional}</p>
                                        <ul class="ml-4 mb-0 fa-ul text-muted">
                                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-id-card"></i></span> DNI: ${usuario.dni}</li>
                                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-birthday-cake"></i></span> Edad: ${usuario.edad}</li>
                                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-building"></i></span> Recidencia: ${usuario.residencia}</li>
                                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-phone"></i></span> Teléfono: ${usuario.telefono}</li>
                                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-at"></i></span> Correo: ${usuario.correo}</li>
                                            <li class="small"><span class="fa-li"><i class="fas fa-lg fa-smile-wink"></i></span> Sexo: ${usuario.sexo}</li>
                                        </ul>
                                    </div>
                                    <div class="col-5 text-center">
                                        <img src="${usuario.avatar}" alt="avatar de usuario" class="img-circle img-fluid">
                                    </div>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="text-right">`;

                if (tipo_usuario == 1) {
                    if (usuario.tipo_usuario != 1) {
                        template += `<button class="borrar-usuario btn btn-danger mr-1" data-toggle="modal" data-target="#confirmar">
                                            <i class="fas fa-window-close mr-1"></i>Eliminar
                                            </button>`;
                    }
                    if (usuario.tipo_usuario == 3 || usuario.tipo_usuario == 4) {
                        template += `<button class="ascender btn btn-primary mr-1" type="button" data-toggle="modal" data-target="#confirmar">
                                            <i class="fas fa-sort-amount-up mr-1"></i>Ascender
                                            </button>`;
                    }
                    if (usuario.tipo_usuario == 2) {
                        template += `<button class="descender btn btn-secondary mr-1" data-toggle="modal" data-target="#confirmar">
                                            <i class="fas fa-sort-amount-down mr-1"></i>Descender
                                            </button>`;
                    }
                } else {
                    if (tipo_usuario == 2 && usuario.tipo_usuario != 2 && usuario.tipo_usuario != 1) {
                        template += `<button class="borrar-usuario btn btn-danger mr-1" data-toggle="modal" data-target="#confirmar">
                                            <i class="fas fa-window-close mr-1"></i>Eliminar
                                            </button>`;
                    }
                }

                template += `</div></div></div></div>`;
            });
            $('#usuarios').html(template);
        });
    }

    $(document).on('keyup', '#buscar', function () {
        let valor = $(this).val();
        buscar_datos(valor);
    });

    $('#form-crear').submit(e => {
        e.preventDefault();
        let nombre = $('#nombre').val();
        let apellido = $('#apellido').val();
        let edad = $('#edad').val();
        let dni = $('#dni').val();
        let pass = $('#pass').val();
        $.post('/usuario/crear', { nombre, apellido, edad, dni, pass }, (response) => {
            if (response.msg === 'usuario_creado') {
                $('#add').fadeIn().delay(2000).fadeOut();
                $('#form-crear').trigger('reset');
                buscar_datos();
            } else {
                $('#noadd').fadeIn().delay(2000).fadeOut();
                $('#form-crear').trigger('reset');
            }
        });
    });

    $(document).on('click', '.ascender', (e) => {
        const elemento = $(e.currentTarget).closest('[usuarioId]');
        const id = $(elemento).attr('usuarioId');
        $('#id_user').val(id);
        $('#funcion').val('ascender');
    });

    $(document).on('click', '.descender', (e) => {
        const elemento = $(e.currentTarget).closest('[usuarioId]');
        const id = $(elemento).attr('usuarioId');
        $('#id_user').val(id);
        $('#funcion').val('descender');
    });

    $(document).on('click', '.borrar-usuario', (e) => {
        const elemento = $(e.currentTarget).closest('[usuarioId]');
        const id = $(elemento).attr('usuarioId');
        $('#id_user').val(id);
        $('#funcion').val('borrar_usuario');
    });

    $('#form-confirmar').submit(e => {
        e.preventDefault();
        let pass = $('#oldpass').val();
        let id_usuario = $('#id_user').val();
        let funcion = $('#funcion').val();
        let url_map = {
            'ascender': '/usuario/ascender',
            'descender': '/usuario/descender',
            'borrar_usuario': '/usuario/borrar'
        };
        let url = url_map[funcion];

        $.post(url, { pass, id_usuario }, (response) => {
            if (response.msg === 'ascendido' || response.msg === 'descendido' || response.msg === 'borrado') {
                $('#confirmado').fadeIn().delay(2000).fadeOut();
            } else {
                $('#rechazado').fadeIn().delay(2000).fadeOut();
            }
            $('#form-confirmar').trigger('reset');
            buscar_datos();
        });
    });
});
