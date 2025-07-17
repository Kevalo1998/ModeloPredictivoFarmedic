$(document).ready(function () {
    $('#cat-carrito').show();
    buscar_producto();
    mostrar_lotes_riesgo();

    function buscar_producto(consulta = '') {
        $.post('/producto/buscar', { consulta: consulta }, (response) => {
            const productos = response;
            let template = ``;
            productos.forEach(producto => {
                template += `
                <div prodId="${producto.id}" prodStock="${producto.stock}" prodNombre="${producto.nombre}" 
                     prodPrecio="${producto.precio}" prodConcentracion="${producto.concentracion}" 
                     prodAdicional="${producto.adicional}" prodLaboratorio="${producto.laboratorio_id}" 
                     prodTipo="${producto.tipo_id}" prodPresentacion="${producto.presentacion_id}" 
                     prodAvatar="${producto.avatar}" 
                     class="col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column">
                    <div class="card bg-light d-flex flex-fill">
                        <div class="card-header text-muted border-bottom-0">
                            <i class="fas fa-lg fa-cubes mr-1"></i>${producto.stock}
                        </div>
                        <div class="card-body pt-0">
                            <div class="row">
                                <div class="col-7">
                                    <h2 class="lead"><b>Código: ${producto.id}</b></h2>
                                    <h2 class="lead"><b>${producto.nombre}</b></h2>
                                    <h4 class="lead"><b><i class="fas fa-lg fa-money-bill-1 mr-1"></i>${producto.precio}</b></h4>
                                    <ul class="ml-4 mb-0 fa-ul text-muted">
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-mortar-pestle"></i></span>Concentración: ${producto.concentracion}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-prescription-bottle"></i></span>Adicional: ${producto.adicional}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-flask"></i></span>Laboratorio: ${producto.laboratorio}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-copyright"></i></span>Tipo: ${producto.tipo}</li>
                                        <li class="small"><span class="fa-li"><i class="fas fa-lg fa-pills"></i></span>Presentación: ${producto.presentacion}</li>
                                    </ul>
                                </div>
                                <div class="col-5 text-center">
                                    <img src="${producto.avatar}" alt="avatar de usuario" class="img-circle img-fluid">
                                </div>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class="text-right">
                                <button class="agregar-carrito btn btn-sm btn-primary">
                                    <i class="fas fa-plus-square mr-2"></i>Agregar al carrito
                                </button>
                            </div>
                        </div>
                    </div>
                </div>`;
            });
            $('#productos').html(template);
        });
    }

    $(document).on('keyup', '#buscar-producto', function () {
        let valor = $(this).val();
        buscar_producto(valor);
    });

    function mostrar_lotes_riesgo() {
        $.post('/lote/riesgo', {}, (response) => {
            const lotes = response;
            let template = '';
            lotes.forEach(lote => {
                let clase = lote.estado === 'warning' ? 'table-warning' : 'table-danger';
                template += `
                <tr class="${clase}">
                    <th>${lote.id}</th>
                    <th>${lote.nombre}</th>
                    <th>${lote.stock}</th>
                    <th>${lote.laboratorio}</th>
                    <th>${lote.presentacion}</th>
                    <th>${lote.proveedor}</th>
                    <th>${lote.mes}</th>
                    <th>${lote.dia}</th>
                </tr>`;
            });
            $('#lotes').html(template);
        });
    }
});