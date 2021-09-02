import math
from PyQt5 import QtWidgets,uic

# Função de validação dos inputs serem números e transformação deles em float        
def ask_numeric_value(text):
    value = ""
    while type(value) != float:
        try:
            value = float(input(text))
        except:
            value = ""
    return value

maj_carga = 1.4 
min_conc = 1.4
min_aço = 1.15

def get_d(h,dl):
    d = h - dl
    return d

def get_md(mk):
    md = maj_carga * mk
    return md

def get_fcd(fck):
    fcd = fck / (10 * min_conc)
    return fcd

def get_fyd(fyk):
    fyd = fyk / min_aço
    return fyd

def get_lam_alf(fck):
    if fck <= 50:
        lambd = 0.8
        alfac = 0.85
    else:
        lambd = 0.8 - ((fck - 50) / 400)
        alfac = 0.85 * (1 - ((fck - 50) / 200))
    return lambd, alfac

def get_delta(h,bw,dl,mk,fck):
    d = get_d(h,dl)
    md = get_md(mk)
    fcd = get_fcd(fck)
    lambd, alfac = get_lam_alf(fck)
    a = 0.5 * (math.pow(lambd, 2)) * alfac * fcd * bw
    b = - lambd * d * alfac * fcd * bw
    c = md
    delta = math.pow(b, 2) - (4 * a * c)
    return a, b, delta

def get_raiz(h,bw,dl,mk,fck):
    a, b, delta = get_delta(h,bw,dl,mk,fck)
    if delta < 0:
        texto = 'Raízes imaginárias, verifique os valores'
        return texto

    if delta == 0:
        raiz = - b / (2 * a)
        texto = 'O valor da LN é (cm): ', raiz
        return texto, raiz

    raiz1 = (- b + math.sqrt(delta)) / (2 * a)
    raiz2 = (- b - math.sqrt(delta)) / (2 * a)
    
    ln_valid = False

    for raiz in [raiz1, raiz2]:
        in_range = raiz >= 0 and raiz <= h
        if in_range:
            #print_root(r)
            texto = 'O valor da LN é (cm): '
            ln_valid = True
            break 

    if ln_valid:
        return texto, raiz

def get_ecu(fck):
    ecu = 0.0026 + (0.035*(((90 - fck) /100) **4))
    return ecu

def get_eyd(fyd):
    eyd = fyd / 210000
    return eyd

def get_x2lim(h,dl,fck):
    d = get_d(h,dl)
    ecu = get_ecu(fck)
    x2lim = (ecu * d) / (0.01 + ecu)
    return x2lim

def get_x3lim(h,dl,fck,fyd):
    d = get_d(h,dl)
    ecu = get_ecu(fck)
    eyd = get_eyd(fyd)
    x3lim = (ecu * d) / (eyd + ecu)
    return x3lim

def get_xlim(h,dl,fck):
    d = get_d(h,dl)
    lim_range = fck >= 20 and fck <= 50
    if lim_range:
        xlim = 0.45*d
    else:
        xlim = 0.35*d
    return xlim

def get_dominio(h,bw,dl,mk,fck,fyd):
    tx, ln = get_raiz(h,bw,dl,mk,fck)
    x2lim = get_x2lim(h,dl,fck)
    x3lim = get_x3lim(h,dl,fck,fyd)
    xlim = get_xlim(h,dl,fck)
    dominio_2 = ln <= x2lim
    dominio_3 = ln >= x2lim and ln <= xlim and ln <= x3lim
    arm_dupla = ln > xlim

    if dominio_2:
        texto = 'Domínio 2'
        return texto
    
    if dominio_3:
        texto = 'Domínio 3'
        return texto

    if arm_dupla:
        texto = 'Armadura Dupla:'
        return texto

def area_aço(h,bw,dl,fck,fyk,mk):
    d = get_d(h,dl)
    fyd = get_fyd(fyk)
    md = get_md(mk)
    lambd, alfac = get_lam_alf(fck)
    texto, ln = get_raiz(h,bw,dl,mk,fck)
    z = d - (0.5 * lambd * ln)
    asi = md / (fyd * z)
    texto = 'A área de aço é (cm²): '
    return texto, z, asi

def arm_dupla(h,bw,dl,fck,fyk,mk):
    d = get_d(h,dl)
    fcd = get_fcd(fck)
    fyd = get_fyd(fyk)
    md = get_md(mk)
    lambd, alfac = get_lam_alf(fck)
    xlim = get_xlim(h,dl,fck)
    ln = xlim
    ecu = get_ecu(fck)
    eyd = get_eyd(fyd)

    m1d = ((lambd*xlim*d)-(0.5*(lambd**2)*(xlim**2)))*alfac*fcd*bw
    m2d = md - m1d

    z = d - (0.5 * lambd * xlim)
    as1 = m1d/(fyd*z)
    as2 = m2d/(fyd*(d-dl))
    ast = as1+as2

    esc = (ecu*(xlim-dl))/xlim
    if esc >= eyd:
        fs = fyd
    else:
        fs = (fyd*esc)/eyd

    asc = m2d/(fs*(d-dl))
    return ast, asc

"""
# Validando inputs com a função
for key in inputs.keys():
    inputs[key]["value"] = ask_numeric_value(inputs[key]["question"])
"""

def main():
    # Tirando variáveis do objeto
    h = float(tela.lineEdit_2.text())
    bw = float(tela.lineEdit_3.text())
    dl = float(tela.lineEdit_4.text())
    mk = float(tela.lineEdit_1.text())
    fck = float(tela.comboBox.currentText())
    fyk = float(tela.comboBox_2.currentText())

    # Extraindo o valor da LN
    texto, ln = get_raiz(h,bw,dl,mk,fck)
    tela.label_12.setText("LN ="+ str('%.2f' % ln))

    # Extraindo o domínio
    fyd = get_fyd(fyk)
    dominio = get_dominio(h,bw,dl,mk,fck,fyd)
    tela.label_13.setText(dominio)

    # Extraindo área de aço
    if dominio == 'Armadura Dupla:':
        ast, asc = arm_dupla(h,bw,dl,fck,fyk,mk)
        ln = get_xlim(h,dl,fck)
        tela.label_12.setText("LN ="+ str('%.2f' % ln))
        tela.label_14.setText("As ="+ str('%.2f' % ast))
        tela.label_17.setText("As' ="+ str('%.2f' % asc))
        tela.label_18.setText("(cm²)")
        
    else:
        texto, z, asi = area_aço(h,bw,dl,fck,fyk,mk)
        tela.label_14.setText("As ="+ str('%.2f' % asi))
        # Falta programar caso não tenha Mk mas tenha As
    
app = QtWidgets.QApplication([])
tela = uic.loadUi('Dimensionamento.ui')

fck_types = ["20","25","30","35","40","45","50","55","60","65","70","75","80","85","90"]
fyk_types = ["25","50","60"]

tela.comboBox.addItems(fck_types)
tela.comboBox_2.addItems(fyk_types)

tela.pushButton.clicked.connect(main)

tela.show()
app.exec()
