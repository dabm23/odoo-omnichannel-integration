# 🛒 Integrador de Ventas Omnicanal para Odoo 18

Este proyecto es un módulo contable desarrollado para Odoo 18 que automatiza la conciliación de ventas provenientes de terminales de pago físicos (TPVs) y canales digitales. 

Diseñado para optimizar la gestión financiera y agilizar la conexión comercial, especialmente adaptado para las lógicas fiscales y de conciliación del mercado en España.

## 🚀 Características Técnicas (Features)

* **Backend & ORM:** Modelado de datos robusto con relaciones `Many2one` y generación de secuencias correlativas automáticas (ej. `TERM/2026/0001`).
* **Motor Contable Automatizado:** Integración directa con el núcleo financiero de Odoo (`account.move`). Generación de asientos contables por partida doble con validaciones de seguridad en Python.
* **Interfaz y UX (XML):** Diseño de vistas `list` y `form` actualizadas a Odoo 18. Implementación de *Smart Buttons* para navegar intuitivamente entre los documentos generados.
* **Motor de Plantillas (QWeb):** Generación de recibos PDF dinámicos.
* **Infraestructura Ágil:** Entorno de desarrollo containerizado listo para usar con Docker Compose (PostgreSQL 15 + Odoo 18).

## 🛠️ Tecnologías Utilizadas
* Python 3
* XML / QWeb (Frontend de Odoo)
* PostgreSQL
* Docker & Docker Compose