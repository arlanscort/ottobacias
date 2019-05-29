'''
    Programa 'otto.py' (maio, 2019)
    Arlan Almeida e Mino Sorribas
    arlan.scortegagna@simepar.br e mino.sorribas@simepar.br
    Sistema Meteorologico do Parana - Simepar
    Siglas:
    BHO - Base Hidrografica Ottocodificada
    ACH - Area de Contribuicao Hidrografica
    TDR - Trecho de Drenagem
    PRJ - Projeto do QGIS (formato .qgz)
    Requisitos:
        - software QGIS
        - software PyQt5
    Entradas:
        - shapefiles contendo as ACHs e TDRs
        - caminhos absolutos do projeto, ACHs e TDRs
    Saidas:
        - shapefile(s) contendo as ACHs a montante da ottobacia selecionada
    Para rodar o programa de dentro do QGIS:
        - Complementos >> Terminal Python >> exec(open('caminho_absoluto/otto.py'.encode('utf-8')).read())
'''

from qgis.core import *
from qgis.utils import *
from PyQt5.QtGui import *
from os import *

### DEFINIR CAMINHOS ABSOLUTOS
path_prj = '/discolocal/arlan/geo/testes_iguacu/teste1.ggz'
path_ach = '/discolocal/arlan/geo/bhos/iguacu/GEOFT_BHO_AREA_CONTRIBUICAO.shp'
path_tdr = '/discolocal/arlan/geo/bhos/iguacu/GEOFT_BHO_TRECHO_DRENAGEM.shp'

### FUNCAO is_outlet
'''
    Entradas:
        - outlet_code - string contendo o codigo de uma ottobacia, ex: '8857'
        - feature_code - string contendo o codigo de uma ottobacia, ex: '8861'
    Resultado:
        - a funcao ira testar se outlet esta a jusante da ottobacia representada por feature_code
'''
def is_outlet(outlet_code, feature_code):
    outlet_code = list(outlet_code)
    feature_code = list(feature_code)
    # trailing = parte do codigo a direita diferente em ambos os codes
    k = []
    for i in range(0,len(outlet_code)):
        try:
            if feature_code[i] != outlet_code[i]:
                k.append(i)
                break
        except:
            continue
    # caso nao tenham sido detectadas diferencas
    if not k:
        if len(feature_code) == 0: # bacia inconsistente (codigo vazio)
            return False
        else: # eh o proprio codigo do outlet (ou um pedaco dele)
            return True
    # caso em que foram detectadas diferencas
    outlet_trailing = outlet_code[k[0]:]
    feature_trailing = feature_code[k[0]:]
    # para ser outlet duas condicoes:
    # c1 :: somente digitos impares em outlet_trailing
    c1 = all(int(n) % 2 == 1 for n in outlet_trailing)
    # c2 :: primeiro digito de outlet_trailing menor do que o primeiro digito de feature_trailing
    c2 = outlet_trailing[0] < feature_trailing[0]
    if c1 & c2:
        return True
    else:
        return False

### EXECUCAO
project = QgsProject.instance()
project.read('prj_folder')
## Abrir o projeto
## Carregar layers
# canvas_layers = [ layer.name() for layer in QgsProject.instance().mapLayers().values() ]
# if ('ach' in canvas_layers) & ('tdr' in canvas_layers):
#     flag_previous = True
#     ach = QgsProject.instance().mapLayersByName('ach')[0]
#     tdr = QgsProject.instance().mapLayersByName('tdr')[0]
# else:
#     flag_previous = False
#     ach = iface.addVectorLayer(path_ach,'','ogr').setName('ach')
#     tdr = iface.addVectorLayer(path_tdr,'','ogr').setName('tdr')
#
# ### SELECAO DA OTTOBACIA DE JUSANTE
# msg = QMessageBox()
# if flag_previous == False:
#     msg.setText('Selecione a bacia de jusante na layer "ach" e rode o programa novamente!')
#     msg.show()
# else:
#     selected_feature = iface.activeLayer().selectedFeatures()
#     if len(selected_feature) != 1:
#         msg.setText('Selecione a ottobacia exutorio (apenas uma)!')
#         msg.show()
#     else:
        ### SELECAO DAS OTTOBACIAS DE MONTANTE
        # selected_feature = selected_feature[0]
        # outlet_code = selected_feature['COBACIA']
        # iface.mapCanvas().setSelectionColor( QColor("red") )
        # upstream_features = []
        # for feature in ach.getFeatures():
        #     feature_code = feature['COBACIA']
        #     if is_outlet(outlet_code, feature_code):
        #         upstream_features.append(feature.id())
        # ach.selectByIds(upstream_features)

        # CRIACAO DO .SHP EM RESULTADOS
        # print ( os.path )

        # try:
        #     os.mkdir(path)
        # except:
        #     pass

        # path_results =
        # QgsVectorFileWriter.writeAsVectorFormat(layer, 'C:/Datasets/South Oxfordshire Clipped LR INSPIRE.shp', "utf-8", None, "ESRI Shapefile", onlySelected=True)

# def we_are_frozen():
#     # All of the modules are built-in to the interpreter, e.g., by py2exe
#     return hasattr(sys, "frozen")
#
# def module_path():
#     encoding = sys.getfilesystemencoding()
#     if we_are_frozen():
#         return os.path.dirname(unicode(sys.executable, encoding))
#
# import module_locator
#
# mypath = module_locator.module_path()
# print(mypath)



exec(open("/discolocal/arlan/programas/github/ottobacias_git/otto.py").read())
