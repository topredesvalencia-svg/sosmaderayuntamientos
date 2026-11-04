"""Textos del kit de contacto con ayuntamientos de SOS Madera."""

EMPRESA = {
    "nombre": "SOS Madera",
    "razon": "SOSMADERA, S.L.",
    "nif": "B26945873",
    "gerentes": "Raúl López · Jose Ferreros",
    "tel": "+34 683 59 77 59",
    "email": "admin@sosmadera.pro",
    "web": "sosmadera.pro",
    "sede": "Bétera (Valencia)",
}

ASUNTO = {
    "Castellano": "Presentación de empresa – Diagnóstico y consolidación de estructuras de madera en edificios municipales",
    "Valenciano": "Presentació d'empresa – Diagnòstic i consolidació d'estructures de fusta en edificis municipals",
}

CARTA = {
    "Castellano": """A la atención de: {destinatario}
Ayuntamiento de {municipio}

{saludo}:

Nos dirigimos a ustedes para presentarles SOS Madera (SOSMADERA, S.L.), empresa con sede en Bétera especializada en el diagnóstico, tratamiento, refuerzo y consolidación de estructuras de madera: forjados, vigas y cubiertas.

Muchos edificios municipales conservan estructuras de madera con décadas o siglos de antigüedad. Con el tiempo aparecen humedades, ataques de xilófagos (carcoma, termitas) o deformaciones que, si no se detectan a tiempo, obligan a cerrar el edificio o a intervenciones mucho más costosas.

Nuestro trabajo cubre todo el proceso:
- Diagnóstico e inspección del estado de la estructura, con informe técnico firmado por arquitecto.
- Tratamiento curativo y preventivo contra xilófagos y hongos.
- Refuerzo y consolidación de vigas y forjados, conservando la madera original siempre que es posible.
{personalizacion}
Les ofrecemos una visita técnica de diagnóstico sin compromiso en el edificio municipal que consideren prioritario. Gran parte de nuestras actuaciones se ajustan al régimen de contrato menor, lo que permite resolverlas con agilidad.

Adjuntamos nuestro dossier de presentación. Quedamos a su disposición para concertar una reunión o visita cuando les resulte conveniente.

Atentamente,

Raúl López · Jose Ferreros
Gerentes – SOS Madera (SOSMADERA, S.L. · NIF B26945873)
Tel. +34 683 59 77 59 · admin@sosmadera.pro · sosmadera.pro
Bétera (Valencia)""",
    "Valenciano": """A l'atenció de: {destinatario}
Ajuntament de {municipio}

{saludo}:

Us escrivim per a presentar-vos SOS Madera (SOSMADERA, S.L.), empresa amb seu a Bètera especialitzada en el diagnòstic, tractament, reforç i consolidació d'estructures de fusta: forjats, bigues i cobertes.

Molts edificis municipals conserven estructures de fusta amb dècades o segles d'antiguitat. Amb el temps apareixen humitats, atacs de xilòfags (corc, tèrmits) o deformacions que, si no es detecten a temps, obliguen a tancar l'edifici o a intervencions molt més costoses.

El nostre treball cobreix tot el procés:
- Diagnòstic i inspecció de l'estat de l'estructura, amb informe tècnic signat per arquitecte.
- Tractament curatiu i preventiu contra xilòfags i fongs.
- Reforç i consolidació de bigues i forjats, conservant la fusta original sempre que és possible.
{personalizacion}
Us oferim una visita tècnica de diagnòstic sense compromís a l'edifici municipal que considereu prioritari. Bona part de les nostres actuacions s'ajusten al règim de contracte menor, cosa que permet resoldre-les amb agilitat.

Adjuntem el nostre dossier de presentació. Restem a la vostra disposició per a concertar una reunió o visita quan us vaja bé.

Atentament,

Raúl López · Jose Ferreros
Gerents – SOS Madera (SOSMADERA, S.L. · NIF B26945873)
Tel. +34 683 59 77 59 · admin@sosmadera.pro · sosmadera.pro
Bètera (València)""",
}

PERSONALIZACION = {
    "Castellano": "\nSabemos que el municipio cuenta con edificios como {edificios}, en los que este tipo de revisión puede ser especialmente útil.\n",
    "Valenciano": "\nSabem que el municipi compta amb edificis com {edificios}, en què aquest tipus de revisió pot ser especialment útil.\n",
}

SALUDO_DEFECTO = {"Castellano": "Estimados/as señores/as", "Valenciano": "Benvolguts/des senyors/es"}
DESTINATARIO_DEFECTO = {
    "Castellano": "Servicios Técnicos Municipales / Concejalía de Urbanismo",
    "Valenciano": "Serveis Tècnics Municipals / Regidoria d'Urbanisme",
}

QUIEN = """
En un ayuntamiento quien decide si se interviene en un forjado o una viga son los **servicios técnicos**, no el alcalde.

| Contacto | Por qué |
| --- | --- |
| Arquitecto/a o arquitecto/a técnico municipal | Contacto principal: detecta patologías, redacta informes y propone actuaciones |
| Concejalía de Urbanismo / Obras y Servicios / Mantenimiento | Gestiona el presupuesto de mantenimiento de edificios |
| Concejalía de Patrimonio o Cultura | Municipios con casco histórico, ermitas, molinos o edificios catalogados |
| Departamento de Contratación | Para entrar en la lista de empresas a las que piden presupuesto en contratos menores |
| Alcaldía o Secretario-Interventor | En pueblos de menos de 5.000 habitantes, sin técnico propio |

Fuera del ayuntamiento: **Diputación** (Cooperación Municipal / Asistencia Técnica a Municipios), **mancomunidades** y la **FVMP**.
"""

QUE = """
**Envío principal**
1. Carta de presentación personalizada (1 página) — en la sección *Generar carta*.
2. Dossier PDF de 4 páginas — en la sección *Dossier*.
3. Oferta de entrada: visita de diagnóstico sin compromiso.

**Contratos menores (LCSP):** hasta 40.000 € sin IVA en obras y 15.000 € en servicios. Adjudicación directa pidiendo presupuestos: es el objetivo principal.
"""

DONDE = """
1. **Sede electrónica → Registro electrónico general / Instancia general**, con el certificado digital de SOSMADERA, S.L. Queda registrado y se asigna a un departamento.
2. **Email directo** a Urbanismo o Servicios Técnicos.
3. **Llamada a la centralita:** «¿Quién es el técnico municipal que lleva el mantenimiento de edificios? ¿Qué días atiende y cuál es su email?»
4. **Plataforma de Contratación del Sector Público:** alertas con «forjado», «madera», «rehabilitación», «cubierta».
"""

COMO_CONTACTO = """
1. Web del ayuntamiento → «Ayuntamiento», «Corporación» o «Directorio»: concejal de Urbanismo / Obras y su email.
2. Sede electrónica → trámite «Instancia general» o «Registro electrónico».
3. Centralita: nombre del arquitecto o aparejador municipal, días de atención y email.
4. Pueblos de la tanda 3: preguntar si el servicio técnico lo presta la Diputación o la mancomunidad.
5. Anotarlo en *Seguimiento* y registrar el envío: la app programa la llamada a los 8 días.
"""

CALENDARIO = [
    ("Semana 1", "Dossier, carta modelo, certificados, seguro e inscripción en registro de licitadores"),
    ("Semana 1–2", "Completar contactos de la tanda 1"),
    ("Semana 2", "Contacto con Diputación y mancomunidades"),
    ("Semana 3–4", "Envío por registro electrónico, unos 10 por semana"),
    ("+7–10 días", "Llamada de seguimiento para pedir cita con el técnico"),
    ("Continuo", "Alertas de licitaciones y recontacto en otoño para presupuestos del año siguiente"),
]

CONSEJOS = """
- **Personalizad la primera línea**: mencionar un edificio concreto multiplica la respuesta.
- **Momento**: los ayuntamientos preparan presupuestos entre septiembre y diciembre.
- **Lenguaje**: técnico con los técnicos («informe de diagnosis», «refuerzo estructural»); de seguridad con alcaldía («evitar cierres»).
- **Valenciano**: en muchos municipios se valora mucho la carta en valenciano o bilingüe.
"""

DOCUMENTACION = [
    "Certificado al corriente con Hacienda",
    "Certificado al corriente con la Seguridad Social",
    "Póliza de responsabilidad civil vigente",
    "Inscripción en ROLECE o Registro de Licitadores de la Comunitat Valenciana",
    "Certificado digital de la empresa operativo",
    "Dossier PDF con fotos reales de obra",
    "Códigos CPV identificados y alertas creadas",
]
