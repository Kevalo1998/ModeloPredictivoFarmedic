$(document).ready(function () {
    calcularTotal();
    RecuperarLsc();
    contador = Contar_productos();
    RecuperarLsc_compra();

    $(document).on('click', '.agregar-carrito', (e) => {
        const elemento = $(this)[0].activeElement.closest('[prodid]');
        const producto = {
            id: $(elemento).attr('prodid'),
            nombre: $(elemento).attr('prodnombre'),
            concentracion: $(elemento).attr('prodconcentracion'),
            adicional: $(elemento).attr('prodadicional'),
            precio: $(elemento).attr('prodprecio'),
            laboratorio: $(elemento).attr('prodlaboratorio'),
            tipo: $(elemento).attr('prodtipo'),
            presentacion: $(elemento).attr('prodpresentacion'),
            avatar: $(elemento).attr('prodavatar'),
            stock: $(elemento).attr('prodstock'),
            cantidad: 1
        };

        const productos = RecuperarLs();
        if (productos.some(p => p.id === producto.id)) {
            Swal.fire({ icon: 'error', title: 'Oops...', text: 'Producto duplicado en carrito.' });
        } else {
            const template = `
                <tr prodid="${producto.id}">
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>${producto.concentracion}</td>
                    <td>${producto.adicional}</td>
                    <td>${producto.precio}</td>
                    <td><button class="borrar-producto btn btn-danger"><i class="fas fa-times-circle"></i></button></td>
                </tr>
            `;
            $('#lista').append(template);
            AgregarLS(producto);
        }
    });

    $(document).on('click', '.borrar-producto', (e) => {
        const elemento = e.target.closest('tr');
        const id = $(elemento).attr('prodid');
        $(elemento).remove();
        Eleminar_prod_ls(id);
    });

    $(document).on('click', '.vaciar-carrito', () => {
        $('#lista').empty();
        Eleminarls();
    });

    $(document).on('click', '#procesar-pedido', () => {
        if (RecuperarLs().length === 0) {
            Swal.fire({ icon: 'error', title: 'Oops...', text: 'No hay productos en el carrito.' });
        } else {
            location.href = '/compra/realizar'; // <-- Ruta Flask
        }
    });

    $(document).on('click', '#procesar-compra', () => {
        procesar_compra();
    });

    function RecuperarLs() {
        return JSON.parse(localStorage.getItem('productos') || '[]');
    }

    function AgregarLS(producto) {
        const productos = RecuperarLs();
        productos.push(producto);
        localStorage.setItem('productos', JSON.stringify(productos));
    }

    function Eleminar_prod_ls(id) {
        const productos = RecuperarLs().filter(p => p.id !== id);
        localStorage.setItem('productos', JSON.stringify(productos));
    }

    function Eleminarls() {
        localStorage.removeItem('productos');
    }

    function Contar_productos() {
        return RecuperarLs().length;
    }

    function RecuperarLsc() {
        const productos = RecuperarLs();
        productos.forEach(producto => {
            $.post('/producto/buscar_id', { id_producto: producto.id }, (response) => {
                const json = response;
                const template = `
                    <tr prodid="${json.id}">
                        <td>${json.id}</td>
                        <td>${json.nombre}</td>
                        <td>${json.concentracion}</td>
                        <td>${json.adicional}</td>
                        <td>${json.precio}</td>
                        <td><button class="borrar-producto btn btn-danger"><i class="fas fa-times-circle"></i></button></td>
                    </tr>
                `;
                $('#lista').append(template);
            });
        });
    }

    function RecuperarLsc_compra() {
        const productos = RecuperarLs();
        productos.forEach(producto => {
            $.post('/producto/buscar_id', { id_producto: producto.id }, (response) => {
                const json = response;
                const template = `
                    <tr prodid="${producto.id}" prodprecio="${json.precio}">
                        <td>${json.nombre}</td>
                        <td>${json.stock}</td>
                        <td class="precio">${Number(json.precio).toFixed(2)}</td>
                        <td>${json.concentracion}</td>
                        <td>${json.adicional}</td>
                        <td>${json.laboratorio}</td>
                        <td>${json.presentacion}</td>
                        <td><input type="number" min="1" class="form-control cantidad_producto" value="${producto.cantidad}"></td>
                        <td class="subtotales"><h5>${(json.precio * producto.cantidad).toFixed(2)}</h5></td>
                        <td><button class="borrar-producto btn btn-danger"><i class="fas fa-times-circle"></i></button></td>
                    </tr>
                `;
                $('#lista-compra').append(template);
            });
        });
    }

    $(document).on('click', '#actualizar', () => {
        const precios = document.querySelectorAll('.precio');
        const productos = RecuperarLs();
        productos.forEach((producto, index) => {
            producto.precio = precios[index].textContent;
        });
        localStorage.setItem('productos', JSON.stringify(productos));
        calcularTotal();
    });

    $('#cp').keyup((e) => {
        const producto = e.target.closest('tr');
        const id = $(producto).attr('prodid');
        const precio = $(producto).attr('prodprecio');
        const cantidad = producto.querySelector('input').value;
        const productos = RecuperarLs();
        const montos = document.querySelectorAll('.subtotales');

        productos.forEach((prod, index) => {
            if (prod.id === id) {
                prod.cantidad = cantidad;
                prod.precio = precio;
                montos[index].innerHTML = `<h5>${(cantidad * precio).toFixed(2)}</h5>`;
            }
        });

        localStorage.setItem('productos', JSON.stringify(productos));
        calcularTotal();
    });

    function calcularTotal() {
        const productos = RecuperarLs();
        const igv = 0.18;
        let total = productos.reduce((sum, prod) => sum + (prod.precio * prod.cantidad), 0);

        const pago = parseFloat($('#pago').val()) || 0;
        const descuento = parseFloat($('#descuento').val()) || 0;

        const con_igv = (total * igv).toFixed(2);
        const subtotal = (total - con_igv).toFixed(2);
        const totalFinal = total - descuento;
        const vuelto = (pago - totalFinal).toFixed(2);

        $('#subtotal').html(subtotal);
        $('#con_igv').html(con_igv);
        $('#total_sin_descuento').html(total.toFixed(2));
        $('#total').html(totalFinal.toFixed(2));
        $('#vuelto').html(vuelto);
    }

    async function Verificar_stock() {
        const productos = RecuperarLs();
        const res = await fetch('/producto/verificar_stock', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ productos })
        });
        return await res.text();
    }

    function procesar_compra() {
        const nombre = $('#cliente').val();
        const dni = $('#dni').val();
        const productos = RecuperarLs();
        if (productos.length === 0) {
            Swal.fire({ icon: 'error', title: 'Oops...', text: 'No hay productos.' }).then(() => {
                location.href = '/catalogo';
            });
        } else if (!nombre) {
            Swal.fire({ icon: 'error', title: 'Oops...', text: 'Ingrese nombre del cliente.' });
        } else {
            Verificar_stock().then(error => {
                if (error == 0) {
                    Registrar_compra(nombre, dni);
                    Swal.fire({ icon: 'success', title: 'Compra realizada correctamente.', showConfirmButton: false, timer: 1500 })
                        .then(() => {
                            Eleminarls();
                            location.href = '/catalogo';
                        });
                } else {
                    Swal.fire({ icon: 'error', title: 'Stock insuficiente' });
                }
            });
        }
    }

    function Registrar_compra(nombre, dni) {
        const total = $('#total').text();
        const productos = RecuperarLs();
        const data = new FormData();
        data.append('nombre', nombre);
        data.append('dni', dni);
        data.append('total', total);
        data.append('json', JSON.stringify(productos));

        $.ajax({
            url: '/venta/registrar_compra',
            type: 'POST',
            data: data,
            processData: false,
            contentType: false
        });
    }
});