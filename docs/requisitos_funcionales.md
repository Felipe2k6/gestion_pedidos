# Requisitos funcionales y diagramas de casos de uso

Estos requisitos y diagramas se elaboraron a partir de las funciones implementadas en la aplicación Django. Los archivos PlantUML están en `docs/uml/`; cada uno corresponde a un requisito.

## Actores

- **Administrador:** gestiona los datos del sistema, puede operar pedidos para clientes y consulta el tablero.
- **Cliente:** consulta productos y gestiona sus propios pedidos.
- **Proveedor:** consulta los productos vinculados a sus recepciones y registra recepciones de mercancía.

Las cuentas las crea el administrador. No hay un flujo de registro público de usuarios.

## Requisitos funcionales

### RF-01 — Autenticación y acceso por rol

El sistema debe permitir que administradores, clientes y proveedores inicien y cierren sesión. Después de autenticar al usuario, debe dirigirlo a las opciones permitidas para su rol y restringir las funciones protegidas a usuarios autenticados.

**Diagrama:** [RF-01 — Acceso y autenticación](uml/RF-01-acceso.puml)

### RF-02 — Administración de clientes, proveedores y cuentas

El administrador debe poder consultar, registrar, editar y eliminar clientes; consultar, registrar y editar proveedores; y consultar usuarios y crear cuentas asignándoles un rol. Las cuentas de cliente y proveedor deben poder vincularse con un registro correspondiente.

**Diagrama:** [RF-02 — Administración de registros y cuentas](uml/RF-02-administracion.puml)

### RF-03 — Catálogo y control de inventario

El sistema debe permitir consultar el catálogo de productos y mantener sus datos según el rol: el administrador puede registrar, editar y eliminar productos; el proveedor puede editar productos vinculados a sus recepciones. El administrador o el proveedor debe poder registrar recepciones de mercancía de un proveedor activo. Al registrarlas, el sistema debe guardar producto, cantidad, costo y fecha, y aumentar el stock. El proveedor solo debe consultar sus propias recepciones y los productos asociados.

**Diagrama:** [RF-03 — Productos y recepción de mercancía](uml/RF-03-inventario.puml)

### RF-04 — Gestión de pedidos

El cliente debe poder crear, consultar y cancelar sus propios pedidos; el administrador debe poder consultar todos los pedidos y crear pedidos para un cliente. El cliente o administrador debe poder agregar productos mientras el pedido no esté cancelado y haya stock suficiente. Al agregar productos, el sistema debe guardar el precio aplicado y descontar el stock. Al cancelar un pedido, debe restaurar las cantidades reservadas. El total debe corresponder a la suma de cantidad por precio guardado en cada detalle.

**Diagrama:** [RF-04 — Ciclo de vida de pedidos](uml/RF-04-pedidos.puml)

### RF-05 — Tablero de gestión

El sistema debe ofrecer al administrador un tablero con el total de clientes y productos, pedidos no cancelados, ingresos de pedidos pendientes, ventas y pedidos por mes de los últimos doce meses, clientes destacados, distribución de clientes por dirección y los cinco pedidos más recientes.

**Diagrama:** [RF-05 — Tablero e indicadores](uml/RF-05-tablero.puml)

## Cómo visualizar o exportar los diagramas

1. Abre la carpeta del proyecto en Visual Studio Code.
2. Instala la extensión **PlantUML**.
3. Abre cualquiera de los archivos `.puml` de `docs/uml/`.
4. Ejecuta **PlantUML: Preview Current Diagram** desde la paleta de comandos (`Ctrl+Shift+P`).
5. Desde la vista previa, usa la opción de exportación para guardar el diagrama como PNG o SVG.

Cada archivo contiene un único diagrama, por lo que puedes previsualizarlos y exportarlos individualmente.
