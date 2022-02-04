from CoolProp.CoolProp import PropsSI
import CoolProp.CoolProp as CP
import pandas as pd
import math

print("Modelamiento matematico final para la tesis - ORC Simple")
print("")
fluidos = ["R717", "R245fa", "R123", "R245ca", "R141b", "R134a", "R22",
           "R152a", "RC318", "R236fa", "R236EA", "R227ea",
           "R124", "R142b", "R290", "Isopentane", "Butane", "Isobutene",
           "n-Pentane", "Benzene", "Cyclopentane", "Toluene"]
contin = 1

while contin == 1:
    "Variables de entrada - foco caliente"
    Te_fc = 390 + 273
    Te_ff = 15 + 273
    mfc = 0.06282608706717943
    print("Los fluidos considerados fueron: 1. R717, 2. R245fa, 3. R123, 4. R245ca, 5. R141b, 6. R134a, \n"
          "7. R22, 8. R152a, 9. RC318, 10. R236fa, 11. R236EA, 12. R227ea, 13. R124, 14. R142b, 15. R290, \n"
          "16. Isopentane, 17. Butane, 18. Isobutene, 19. n-Pentane, 20. Benzene, 21. Cyclopentane, 22. Toluene")
    print("")
    a = int(input("De los fluidos considerados, seleccione 1 (Del 1 al 22): "))
    fluido = fluidos[int(a - 1)]

    "Condiciones de diseño"
    eta_bomba = 0.7
    eta_turbina = 0.7
    eta_generador = 0.93
    Tppmin_eva = 30 + 273
    Tppmin_cond = 5 + 273
    Tconden = 35 + 273
    Pconden = PropsSI('P', 'T', Tconden, 'Q', 0, fluido)

    "Calor especifico de los gases de escape"
    Cp_fc = 1048.9336359934507
    Cp_ff = 4.189 * 1000

    print("")
    print("Condiciones de trabajo para el fluido: ", fluido)

    "Ciclo termodinamico"

    "Punto 1"
    P_1 = Pconden
    T_1 = Tconden
    h_1 = PropsSI('H', 'T', T_1, 'Q', 0, fluido)

    "Punto 2"
    Pbomba = 0.9 * CP.PropsSI("Pcrit", fluido)
    P_2 = Pbomba

    "Zona de la bomba"
    V_fluido = 1 / PropsSI('D', 'T', T_1, 'P', P_2, fluido)
    ws_bomba = V_fluido * (P_2 - P_1)
    hs_2 = ws_bomba + h_1
    h_2 = ((hs_2 - h_1) / eta_bomba) + h_1
    T_2 = PropsSI('T', 'P', P_2, 'H', h_2, fluido)

    "Punto 3"
    P_3 = P_2
    T_3 = PropsSI('T', 'P', P_3, 'Q', 1, fluido)
    h_3 = PropsSI('H', 'T', T_3, 'Q', 1, fluido)

    "Zona del evaporador"

    "Analisis del punto Pinch del evaporador"

    Tx_2 = T_3
    hx_2 = PropsSI('H', 'T', Tx_2, 'Q', 0, fluido)
    Tpp_fc = Tx_2 + (Tppmin_eva - 273)

    "Balance 1: Zona de Vaporización del fluido"

    a = mfc * Cp_fc * (Te_fc - Tpp_fc)
    b = (h_3 - hx_2)
    mciclo = a / b

    "Balance 2: Zona de precalentamiento del fluido"
    c = hx_2 - h_2
    d = mfc * Cp_fc
    Ts_fc = Tpp_fc - mciclo * (c / d)

    i = 0
    a = 1
    while a == 1:
        if Ts_fc <= 393:
            mciclo = mciclo * 0.99
            Tpp_fc = Te_fc - mciclo * ((h_3 - hx_2) / (mfc * Cp_fc))
            Ts_fc = Tpp_fc - mciclo * (c / d)
            i = i + 1
        else:
            a = 0

    "Calculo del area"
    "Zona de Evaporacion"
    Ueva_evap = 99
    Qeva_evap = mciclo * (h_3 - hx_2)
    TA = Tpp_fc - Tx_2
    TB = Te_fc - T_3
    DelTevap_evap = (TA - TB) / math.log(TA / TB)
    Aeva_evap = Qeva_evap / (DelTevap_evap * Ueva_evap)

    "Zona de precalentamiento"
    Ueva_pre = 99
    Qeva_pre = mciclo * (hx_2 - h_2)
    TA = Ts_fc - T_2
    TB = Tpp_fc - Tx_2
    DelTevap_pre = (TA - TB) / math.log(TA / TB)
    Aeva_pre = Qeva_pre / (DelTevap_pre * Ueva_pre)

    At_evapor = Aeva_pre + Aeva_evap

    print("")
    print("Analisis Pinch del evaporador")
    print("Temperatura de entrada de los gases: ", Te_fc - 273, " °C")
    print("Temperatura punto pinch gases: ", Tpp_fc - 273, " °C")
    print("Temperatura de salida del gas: ", Ts_fc - 273, " °C")
    print("Flujo masico del fluido de trabajo: ", mciclo, " kg/s")
    print("Area necesaria en la zona de precalentamiento: ", Aeva_pre, " m2")
    print("Area necesaria en la zona de evaporacion: ", Aeva_evap, " m2")
    print("Nueva diferencia de temperatura en el punto pinch:", (Tpp_fc - Tx_2), " °C")
    print("Numero de iteraciones para la condición de salida del gas: ", i)
    print("")

    "Zona de la turbina"
    s_3 = PropsSI('S', 'T', T_3, 'Q', 1, fluido)
    ss_4 = s_3
    P_4 = Pconden
    hs_4 = PropsSI('H', 'P', P_4, 'S', ss_4, fluido)
    ws_turbina = -(hs_4 - h_3) * mciclo
    h_4 = h_3 - eta_turbina * (h_3 - hs_4)
    T_4 = PropsSI('T', 'H', h_4, 'P', P_4, fluido)

    "Zona del condensador"

    "Analisis Pinch en el condensador"

    Ts_ff = 374
    i = 0
    Acond_sobre = 0

    if T_4 / T_1 < 1.00001:
        print("Fluido Isoentrópico")
        "Solo hay zona de vaporización"
        Ts_ff = T_4 - (Tppmin_cond - 273)
        hff_e = PropsSI('H', 'P', P_4, 'T', Te_ff, "Water")
        hff_s = PropsSI('H', 'P', P_4, 'T', Ts_ff, "Water")
        a = mciclo * (h_4 - h_1)
        b = hff_s - hff_e
        mff = a / b
        Tpp_ff = Ts_ff

        "Calculo del area"
        Ucond_conden = 746  # W/m2-K
        Qcond_conden = mff * (hff_s - hff_e)
        TA = T_1 - Te_ff
        TB = T_4 - Ts_ff
        DelTcond_conden = (TA - TB) / math.log(TA / TB)
        Acond_condensa = Qcond_conden / (DelTcond_conden * Ucond_conden)

        At_conden = Acond_condensa

    else:
        print("Fluido Seco")
        Tx_4 = T_1
        hx_4 = PropsSI('H', 'T', Tx_4, 'Q', 1, fluido)
        Tpp_ff = Tx_4 - (Tppmin_cond - 273)  # Temperatura punto pinch

        "Balance 2: Zona de condensación del fluido"

        a = mciclo * (hx_4 - h_1)
        hff_e = PropsSI('H', 'P', P_4, 'T', Te_ff, "Water")
        hff_pp = PropsSI('H', 'P', P_4, 'T', Tpp_ff, "Water")
        b = hff_pp - hff_e
        mff = a / b

        "Balance 2: Zona de sobrecalentamiento del fluido"
        c = (h_4 - hx_4)
        d = mff * Cp_ff
        Ts_ff = Tpp_ff + mff * (c / d)

        "Calculo del area"
        "Zona de condensación"
        Ucond_conden = 746  # W/m2-K
        Qcond_conden = mff * (hff_pp - hff_e)
        TA = T_1 - Te_ff
        TB = Tx_4 - Tpp_ff
        DelTcond_conden = (TA - TB) / math.log(TA / TB)
        Acond_condensa = Qcond_conden / (DelTcond_conden * Ucond_conden)

        "Zona de sobrecalentamiento"
        Ucond_sobre = 746  # W/m2-K
        hff_s = PropsSI('H', 'P', P_4, 'T', Ts_ff, "Water")
        Qcond_sobre = mff * (hff_s - hff_pp)
        TA = Tx_4 - Tpp_ff
        TB = T_4 - Ts_ff
        DelTcond_sobre = (TA - TB) / math.log(TA / TB)
        Acond_sobre = Qcond_sobre / (DelTcond_sobre * Ucond_sobre)

        At_conden = Acond_sobre + Acond_condensa

    print("Analisis Pinch del condensador")
    print("Temperatura de entrada del agua: ", Te_ff - 273, " °C")
    print("Temperatura punto pinch del agua: ", Tpp_ff - 273, " °C")
    print("Temperatura de salida del agua: ", Ts_ff - 273, " °C")
    print("Flujo masico del agua: ", mff, " kg/s")
    print("Area necesaria en la zona de sobrecalentamiento: ", Acond_sobre, " m2")
    print("Area necesaria en la zona de condensación: ", Acond_condensa, " m2")
    print("Numero de iteraciones para la condición de salida del agua: ", i)
    print("")

    print("Rendimiento")
    Wbomba = mciclo * (h_2 - h_1)
    print("Trabajo de la bomba: ", Wbomba / 1000, " kW")
    Wturbina = mciclo * (h_3 - h_4)
    print("Trabajo de la turbina: ", Wturbina / 1000, " kW")
    Qconden = mciclo * (h_4 - h_1)
    print("Calor rechazado en el condensador: ", Qconden / 1000, " kW")
    Qevapor = mciclo * (h_3 - h_2)
    print("Calor entregado en el evaporador: ", Qevapor / 1000, " kW")
    Wneto = Wturbina - Wbomba
    print("Trabajo neto: ", Wneto / 1000, " kW")
    Welectric = eta_generador * Wneto
    print("Energía electrica generada: ", Welectric / 1000, " kW")
    eficiencia = Wneto / Qevapor
    print("Eficiencia: ", eficiencia * 100, " %")
    print("Area de evaporador: ", At_evapor, " m2")
    print("Area de condensador: ", At_conden, " m2")

    print("")

    # Guardar los resultados en arrays
    entalpias = [h_1 / 1000, h_2 / 1000, h_3 / 1000, h_4 / 1000]
    temperaturas = [T_1 - 273, T_2 - 273, T_3 - 273, T_4 - 273]
    presiones = [P_1 / 1000, P_2 / 1000, P_3 / 1000, P_4 / 1000]

    resultados = {"Temperaturas [°C]": temperaturas, "Presiones [kPa]": presiones,
                  "Entalpias [kJ/kg]": entalpias}  # Indices de los arrays

    data_frameResultados = pd.DataFrame(resultados, index=[1, 2, 3, 4])  # Comado para mostrarlo como tabla
    print("Resultados del ciclo en cada punto")
    print(data_frameResultados)
    print("")
    print("Punto 1: Salida del condensador")
    print("Punto 2: Salida de la bomba")
    print("Punto 3: Salida del evaporador")
    print("Punto 4: Salida de la turbina")

    print("")
    print("Costos")
    "Actualización de costos"
    Actu2020 = 607.5 / 596.2
    "Costos de los componentes"
    "Turbina"
    k1 = 2.2476
    k2 = 1.4965
    k3 = -0.1618
    logC_turb = k1 + k2 * math.log10(Wturbina / 1000) + k3 * (math.log10(Wturbina / 1000) ** 2)
    C_turb = 10 ** logC_turb
    "Condensador"
    Cr_conden = 10000 + 324 * (At_conden ** 0.91)
    "Bomba"
    k1 = 3.3892
    k2 = 0.0536
    k3 = 0.1538
    logC_bomb = k1 + k2 * math.log10(Wbomba / 1000) + k3 * (math.log10(Wbomba / 1000) ** 2)
    Cr_bomb = 10 ** logC_bomb
    "Evaporador"
    Cr_evapo = 10000 + 324 * (At_evapor ** 0.91)
    "Generador"
    C_generador = 60 * (Welectric / 1000) ** 0.95
    "Costo total"
    Ctotal_equipos = (C_turb + Cr_conden + Cr_bomb + Cr_evapo + C_generador) * Actu2020
    Ctotal_OM = Ctotal_equipos * 0.0168  # Operación y mantenimiento
    Ctotal_invers = Ctotal_equipos + Ctotal_OM  # Costo de inversion total
    Ctotal_invers_uni = Ctotal_invers / (Wneto / 1000)
    "Costos de inversion de capital anuales"
    i = 0.06
    n = 20
    a = i * ((1 + i) ** n)
    b = ((1 + i) ** n) - 1
    CRF = a / b  # Capital Recovery Factor - Pasar a anualidades el costo total
    C_inveEqui = CRF * Ctotal_equipos
    C_OM = C_inveEqui * 0.015
    C_total = C_inveEqui + C_OM  # Costo total pasado ya a anualidades
    "Energía generada en un año"
    E_anual = (Welectric / 1000) * 7500
    "Costos de inversion por energía generada"
    Ctotal_E = C_total / E_anual

    costos_inversion = {"Costo de inversion [USD]": [C_turb, Cr_conden, Cr_bomb, Cr_evapo, C_generador,
                                                     Ctotal_equipos, Ctotal_OM, Ctotal_invers]}

    costos_inversion_index = ["Costo turbina", "Costo del condensador",
                              "Costo de la bomba", "Costo del evaporador", "Costo del generador",
                              "Costo total equipos", "Costo de OyM", "Costo total inversion"]

    data_frameCostos_inversion = pd.DataFrame(costos_inversion, index=costos_inversion_index)
    print("")
    print("Distribucion de costos de inversion")
    print(data_frameCostos_inversion)
    print("")
    print("Costo unitario de inversion: ", Ctotal_invers_uni, " [USD/kW]")
    print("")
    print("Costos anuales")
    print("Costos de inversión de equipos: ", C_inveEqui, " [USD/año]")
    print("Costos de operacion y mantenimiento: ", C_OM, " [USD/año]")
    print("Costos de inversion total: ", C_total, " [USD/año]")
    print("Energía generada anual: ", E_anual, " [kWh/año]")
    print("Costo nivelado de energía: ", Ctotal_E, " [USD/kWh-año]")
    print("")

    "Datos del motor"
    PotGene = 32  # kW
    PCI = 42886.8  # kJ/kg
    mfuel = 0.002603125  # kg/s
    EnergiaIn = PCI * mfuel
    eta_motor = PotGene / EnergiaIn
    print("Eficiencia del motor sin ORC: ", eta_motor * 100, " %")
    eta_motor2 = (PotGene + (Welectric / 1000)) / EnergiaIn
    print("Eficiencia del sistema M-ORC: ", eta_motor2 * 100, " %")
    NuevaEfici = eta_motor2 - eta_motor
    print("Aumento en la eficiencia: ", NuevaEfici * 100, " %")

    print("")
    "Costos del motor"
    Cinstalacion_uni = 532 * PotGene * CRF  # $inver/año #532usd/kw
    COyM_uni = 27 * (PotGene / 1000) * 7500  # Ya están anuales #27usd/MWh-gener
    Cfuel = 0.591  # $/L
    FlujoVfuel = ((75 / 1000) / 24)  # L/s
    Cfuel_2 = FlujoVfuel * 3600 * 7500 * Cfuel  # $/año

    Ctotal_año = Cinstalacion_uni + COyM_uni + Cfuel_2
    E_geneMotor_año = PotGene * 7500
    print("Producción de energía anual del motor:", E_geneMotor_año / 1000, " [MWh-año]")
    LCOEmotor = Ctotal_año / E_geneMotor_año
    print("Costo nivelado del motor solo:", LCOEmotor, " [USD/kWh-año]")
    LCOEtotal = (Ctotal_año + C_total) / (E_geneMotor_año + E_anual)
    print("Costo nivelado del conjunto:", LCOEtotal, " [USD/kWh-año]")
    LCOEahorrado = LCOEmotor - LCOEtotal
    print("Costo nivelado ahorrado por la implementación del ORC:", LCOEahorrado, " [USD/kWh-año]")
    PorcenAhorro = LCOEahorrado / LCOEmotor
    print("Porcentaje reducido: ", PorcenAhorro * 100, " [%]")
    DineroAhorrado = LCOEahorrado * (E_geneMotor_año + E_anual)
    print("Dinero ahorrado anual por el ORC: ", DineroAhorrado, " [USD/año]")
    print("")

    "Combustible"

    ConsuFuelUni = (75 / 1000) / (PotGene * 7500)  # L/kWh
    print("Consumo combustible unitario del motor: ", ConsuFuelUni, " [L/kWh]")
    ConsuFuelUni_ORC = (75 / 1000) / ((PotGene + (Welectric / 1000)) * 7500)
    print("Consumo combustible unitario del motor-ORC: ", ConsuFuelUni_ORC, " [L/kWh]")
    AhorroFuel = (ConsuFuelUni - ConsuFuelUni_ORC) / ConsuFuelUni
    print("Porcentaje de ahorro de combustible: ", AhorroFuel * 100, " [%]")

    print("")
    "Emisiones totales del motor"
    Cfuel_anual = FlujoVfuel * 3600 * 7500  # L/año
    Cfuel_anual_gal = Cfuel_anual / 3.785  # Gal/año
    FCH4 = 28
    FN2O = 265
    EmisionsCO2 = 10.2765 * Cfuel_anual_gal  # kgCO2/año
    EmisionsCH4 = (0.0096 / 1000) * Cfuel_anual_gal  # kgCH4/año
    EmisionsN2O = (0.0058 / 1000) * Cfuel_anual_gal  # kgN2O/año
    EmisionsT_motor = EmisionsCO2 + (EmisionsCH4 * FCH4) + (EmisionsN2O * FN2O)  # kgCO2equi
    print("Emisiones del motor: ", EmisionsT_motor / 1000, " tCO2equi/año")
    "Emisiones unitarias"
    EmisionesMotor_uni = EmisionsT_motor / (PotGene * 3600)  # kgCO2equi/kwh-año
    print("Emisiones unitarias del motor: ", EmisionesMotor_uni, " kgCO2equi/kWh-año")
    EmisionesMotorORC_uni = EmisionsT_motor / ((PotGene + (Welectric / 1000)) * 3600)
    print("Emsiones unitarias del motor-ORC: ", EmisionesMotorORC_uni, " kgCO2equi/kWh-año")
    EmisionesSaves = EmisionesMotor_uni - EmisionesMotorORC_uni
    print("Emsiones dejadas de emitir: ", EmisionesSaves, " kgCO2equi/kWh-año")
    AhorroEmisiones = (EmisionesMotor_uni - EmisionesMotorORC_uni) / EmisionesMotor_uni
    print("Porcentaje de emisiones dejadas de emitir: ", AhorroEmisiones * 100, " [%]")
    EmisionesSavesT = EmisionesSaves * ((PotGene + (Welectric / 1000)) * 3600)
    print("Emisiones totales dejadas de emitir: ", EmisionesSavesT / 1000, " tCO2equi/año")
    EmisioneSistema = EmisionsT_motor - EmisionesSavesT
    print("Emisiones nueva del sistema Motor-ORC: ", EmisioneSistema / 1000, " tCO2equi/año")

    "Equivalencia de árboles"
    EmisionsFactTree = 26.635  # kgCO2-año/arbol
    TreeSaves = EmisionesSavesT / EmisionsFactTree
    print("Equivalencia de árboles plantados por CO2 no emitido: ", TreeSaves, " Árboles")

    print("")
    if DineroAhorrado > 0:
        "Indicadores economicos"
        Payback = Ctotal_invers / DineroAhorrado
        print("Los años en lo que se recupera la inversión: ", round(Payback, 2), " Años")
    else:
        print("Con ese fluido no es viable el proyecto")
    print("")

    contin = int(input("¿Quiere intentar con otro fluido?, Sí=1, No=0: "))
    while contin < 0 or contin > 1:
        contin = int(input("¿Elija un valor entre 1 y 2?, Sí=1, No=0: "))





