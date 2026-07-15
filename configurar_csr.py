# configurar_csr.py
# Script de examen DRY7122 para automatizar configuraciones en CSR1000v vía NETCONF

from ncclient import manager
import xml.dom.minidom

# --- DATOS DE CONEXIÓN AL ROUTER CSR1000v ---
HOST = "192.168.56.108"
PORT = 830               # Puerto estándar de NETCONF
USER = "cisco"       # Usuario configurado en el router
PASSWORD = "cisco123"  # Contraseña del usuario

# Apellidos de los integrantes del grupo para el nuevo Hostname
APELLIDOS_GRUPO = "ChuHan"

# --- PLANTILLA XML COMPATIBLE (Cisco-IOS-XE-native) ---
# Se estructura 'hostname' directamente bajo 'native' para evitar el error de 'system'
config_xml = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>{APELLIDOS_GRUPO}</hostname>
    <interface>
      <Loopback>
        <name>111</name>
        <ip>
          <address>
            <primary>
              <address>111.111.111.111</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

print(f"Iniciando conexión NETCONF hacia {HOST}:{PORT}...")

try:
    # Establecer la sesión NETCONF mediante SSH
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:
        
        print("¡Conexión NETCONF establecida con éxito!")
        print("Enviando configuración XML al router (Hostname y Loopback 111)...")
        
        # Enviar la configuración al Running-Config del router
        respuesta_netconf = m.edit_config(target='running', config=config_xml)
        
        # Parsear la respuesta para confirmar que fue exitosa
        xml_pretty = xml.dom.minidom.parseString(respuesta_netconf.xml).toprettyxml()
        
        if "<ok/>" in respuesta_netconf.xml:
            print("\n========================================================")
            print("  ¡CONFIGURACIÓN APLICADA EXITOSAMENTE EN EL ROUTER!   ")
            print("========================================================")
            print(f"-> El nuevo Hostname es: {APELLIDOS_GRUPO}")
            print("-> Interfaz Loopback 111 creada con IP: 111.111.111.111/32")
            print("========================================================\n")
        else:
            print("Error en la configuración. Respuesta del Router:")
            print(xml_pretty)

except Exception as e:
    print(f"\nError al conectar o configurar el router: {e}")
    print("Verifique la IP del router, las credenciales, y asegúrese de que 'netconf-yang' esté habilitado en el CSR1000v.")
