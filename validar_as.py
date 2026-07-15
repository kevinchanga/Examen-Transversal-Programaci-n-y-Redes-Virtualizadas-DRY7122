# validar_as.py
# Script para verificar si un ASN (Autonomous System Number) es Público o Privado

print("--- Validador de ASN BGP ---")

try:
    asn = int(input("Ingrese el número de AS de BGP a verificar: "))
    
    # Validación de rangos privados (16-bit y 32-bit)
    is_private_16bit = (64512 <= asn <= 65534)
    is_private_32bit = (4200000000 <= asn <= 4294967294)
    
    # Rango máximo permitido para ASN
    if asn < 1 or asn > 4294967295:
        print("Error: El número de AS ingresado está fuera del rango válido global (1 - 4294967295).")
    elif is_private_16bit or is_private_32bit:
        print(f"El AS {asn} es un AS PRIVADO.")
    else:
        print(f"El AS {asn} es un AS PÚBLICO.")

except ValueError:
    print("Error: Por favor, ingrese un número entero válido.")
