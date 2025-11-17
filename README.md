# product_website_customer_visibility

Módulo de Odoo 15 para controlar la visibilidad de productos en el sitio web según clientes específicos.

## Funcionalidades
- Nuevos campos en **Productos**:
  - **Visible para todos los clientes**: bandera para mantener el comportamiento estándar.
  - **Clientes permitidos**: lista Many2many de clientes autorizados a ver el producto cuando la bandera anterior está desactivada.
- Filtrado automático en catálogos y búsquedas del eCommerce para mostrar solo productos visibles para el cliente conectado (o públicos cuando no hay sesión), manteniendo las restricciones de categorías y grupos ya existentes.
- Edición de visibilidad disponible en la pestaña **Website** del formulario de producto.

## Instalación
1. Coloca este módulo en la ruta de addons de tu instancia de Odoo 15.
2. Actualiza la lista de apps y busca **Product Website Customer Visibility**.
3. Instala el módulo (requiere dependencia `website_sale`).

## Configuración
1. Abre **Ventas > Productos** y edita un producto.
2. En la pestaña **Website**, sección **Visibilidad por cliente**:
   - Deja activado **Visible para todos los clientes** para mostrarlo a cualquiera.
   - Desactiva la casilla y selecciona los **Clientes permitidos** que podrán ver y comprar el producto en el eCommerce.
3. Inicia sesión como un cliente permitido para validar que el producto aparece en el catálogo y en los resultados de búsqueda. Otros clientes no lo verán.

## Notas
- Los productos siguen respetando restricciones de categorías, grupos y publicación de website. Este módulo solo añade una capa adicional de filtrado por cliente.
