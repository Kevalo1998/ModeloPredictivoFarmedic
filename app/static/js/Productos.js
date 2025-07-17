$(document).ready(function(){
    let tipo_usuario = $('#tipo_usuario').val();
    let edit = false;
    $('.select2').select2();
    rellenar_laboratorios();
    rellenar_tipos();
    rellenar_presentaciones();
    rellenar_proveedores();
    buscar_producto();
    if (['2','3','4'].includes(tipo_usuario)) {
        $('#bcp').hide();
    }
    function rellenar_laboratorios() {
        $.post('/laboratorio/rellenar', {}, (response) => {
            let template = '';
            response.forEach(lab => {
                template += `<option value="${lab.id}">${lab.nombre}</option>`;
            });
            $('#modal_laboratorio').html(template);
        });
    }
    function rellenar_tipos() {
        $.post('/tipo/rellenar', {}, (response) => {
            let template = '';
            response.forEach(tipo => {
                template += `<option value="${tipo.id}">${tipo.nombre}</option>`;
            });
            $('#modal_tipo').html(template);
        });
    }

    function rellenar_presentaciones() {
        $.post('/presentacion/rellenar', {}, (response) => {
            let template = '';
            response.forEach(pres => {
                template += `<option value="${pres.id}">${pres.nombre}</option>`;
            });
            $('#modal_presentacion').html(template);
        });
    }
    function rellenar_proveedores() {
    $.post('/producto/rellenar_proveedores', {}, (response) => {
        let template = '';
        response.forEach(prov => {
            template += `<option value="${prov.id}">${prov.nombre}</option>`;
        });
        $('#proveedor').html(template);
    });
    }
    $('#form-crear-producto').submit(e => {
        e.preventDefault();
        let data = {
            id: $('#id_edit_prod').val(),
            nombre: $('#nombre_producto').val(),
            concentracion: $('#concentracion').val(),
            adicional: $('#adicional').val(),
            precio: $('#precio').val(),
            laboratorio: $('#modal_laboratorio').val(),
            tipo: $('#modal_tipo').val(),
            presentacion: $('#modal_presentacion').val()
        };
        const ruta = edit ? '/producto/editar' : '/producto/crear';

        $.post(ruta, data, (res) => {
            if (res.msg === 'add') {
                $('#add').hide('slow').show(1000).hide(2000);
            } else if (res.msg === 'edit') {
                $('#edit_prod').hide('slow').show(1000).hide(2000);
            } else {
                $('#noadd').hide('slow').show(1000).hide(2000);
            }
            $('#form-crear-producto').trigger('reset');
            edit = false;
            buscar_producto();
        });
    });
    function buscar_producto(consulta = '') {
        $.post('/producto/buscar', { consulta }, (productos) => {
            let template = '';
            console.log(productos);
            productos.forEach(p => {
                template += `
                <div prodId="${p.id}" prodNombre="${p.nombre}" prodPrecio="${p.precio}" prodConcentracion="${p.concentracion}" prodAdicional="${p.adicional}" prodLaboratorio="${p.laboratorio_id}" prodTipo="${p.tipo_id}" prodPresentacion="${p.presentacion_id}" prodAvatar="${p.avatar}" class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                    <div class="card bg-light d-flex flex-fill">
                        <div class="card-header text-muted border-bottom-0">
                            <i class="fas fa-lg fa-cubes mr-1"></i>${p.stock}
                        </div>
                        <div class="card-body pt-0">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="lead"><b>${p.nombre}</b></h2>
                                    <h4 class="lead"><b><i class="fas fa-lg fa-money-bill-1 mr-1"></i>${p.precio}</b></h4>
                                    <ul class="ml-4 mb-0 fa-ul text-muted">
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-mortar-pestle"></i></span>Concentración: ${p.concentracion}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-prescription-bottle"></i></span>Adicional: ${p.adicional}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-flask"></i></span>Laboratorio: ${p.laboratorio}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-copyright"></i></span>Tipo: ${p.tipo}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-pills"></i></span>Presentación: ${p.presentacion}</li>
                                    </ul>
                                </div>
                                <div class="col-5 text-center">
                                    <img src="${p.avatar}" alt="avatar" class="img-circle img-fluid">
                                </div>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class="text-right">`;
                if (tipo_usuario == 1) {
                    template += `
                        <button class="avatar btn btn-sm bg-teal" data-toggle="modal" data-target="#cambiologoip"><i class="fas fa-image"></i></button>
                        <button class="editar btn btn-sm btn-success" data-toggle="modal" data-target="#crearproducto"><i class="fas fa-pencil-alt"></i></button>
                        <button class="lote btn btn-sm btn-primary" data-toggle="modal" data-target="#crearlote"><i class="fas fa-plus-square"></i></button>
                        <button class="borrarip btn btn-sm btn-danger"><i class="fas fa-trash-alt"></i></button>`;
                }
                template += `</div></div></div></div>`;
            });
            $('#productos').html(template);
        });
    }
    $(document).on('keyup', '#buscar-producto', function(){
        buscar_producto($(this).val());
    });
    $(document).on('click', '.avatar', function(){
        const el = $(this).closest('[prodId]');
        $('#funcionip').val('cambiar_avatar');
        $('#id_logo_prod').val(el.attr('prodId'));
        $('#avatarip').val(el.attr('prodAvatar'));
        $('#logoactual_ip').attr('src', el.attr('prodAvatar'));
        $('#nombre_logoip').html(el.attr('prodNombre'));
    });
    $('#form-logo-ip').submit(e => {
        const formData = new FormData($('#form-logo-ip')[0]);
        $.ajax({
            url: '/producto/cambiar_avatar',
            type: 'POST',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: (res) => {
                if (res.alert === 'edit') {
                    $('#logoactual_ip').attr('src', res.ruta);
                    $('#editip').hide('slow').show(1000).hide(2000);
                    buscar_producto();
                } else {
                    $('#noeditip').hide('slow').show(1000).hide(2000);
                }
                $('#form-logo-ip').trigger('reset');
            }
        });
        e.preventDefault();
    });
    $(document).on('click', '.editar', function(){
        const el = $(this).closest('[prodId]');
        $('#id_edit_prod').val(el.attr('prodId'));
        $('#nombre_producto').val(el.attr('prodNombre'));
        $('#concentracion').val(el.attr('prodConcentracion'));
        $('#adicional').val(el.attr('prodAdicional'));
        $('#precio').val(el.attr('prodPrecio'));
        $('#modal_laboratorio').val(el.attr('prodLaboratorio')).trigger('change');
        $('#modal_tipo').val(el.attr('prodTipo')).trigger('change');
        $('#modal_presentacion').val(el.attr('prodPresentacion')).trigger('change');
        edit = true;
    });
    $(document).on('click', '.borrarip', function(){
        const el = $(this).closest('[prodId]');
        const id = el.attr('prodId');
        const nombre = el.attr('prodNombre');
        const avatar = el.attr('prodAvatar');

        Swal.fire({
            title: `Eliminar ${nombre}?`,
            text: 'No se puede recuperar esto',
            imageUrl: avatar,
            showCancelButton: true,
            confirmButtonText: '¡Sí, borrar!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.post('/producto/borrar', {id}, (res) => {
                    if (res.msg === 'borrado') {
                        Swal.fire('¡Borrado!', `${nombre} fue eliminado.`, 'success');
                        buscar_producto();
                    } else {
                        Swal.fire('Error', `No se puede borrar ${nombre}, tiene lotes registrados.`, 'error');
                    }
                });
            }
        });
    });
    $(document).on('click', '.lote', function(){
        const el = $(this).closest('[prodId]');
        $('#id_lote_prod').val(el.attr('prodId'));
        $('#nombre_producto_lote').html(el.attr('prodNombre'));
    });
    $('#form-crear-lote').submit(e => {
    e.preventDefault();
    let data = {
        id_producto: $('#id_lote_prod').val(),
        proveedor: $('#proveedor').val(),
        stock: $('#stock').val(),
        vencimiento: $('#vencimiento').val()
    };

    console.log(data);  // Verifica que proveedor sea un id numérico

    $.post('/lote/crear', data, (res) => {
        $('#add-lote').hide('slow').show(1000).hide(2000);
        $('#form-crear-lote').trigger('reset');
        buscar_producto();
    });
});
});