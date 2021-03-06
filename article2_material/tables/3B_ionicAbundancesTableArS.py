from dazer_methods import Dazer
from collections import OrderedDict
from lib.inferenceModel import SpectraSynthesizer
from pylatex import Package
import uncertainties


def checkDictValue(inputDict, variable, emptyValue='-'):
    outputVariable = '-'

    if variable in inputDict:
        outputVariable = uncertainties.ufloat(inputDict[variable][0], inputDict[variable][1])

    return outputVariable


# Headers
headers_dic                     = OrderedDict()
headers_dic['S2']          = r'$12 + log\left(\nicefrac{S^{+}}{H^{+}}\right)$'
headers_dic['S3']         = r'$12 + log\left(\nicefrac{S^{2+}}{H^{+}}\right)$'
headers_dic['ICF_SIV']          = r'$ICF\left(S^{3+}\right)$'
headers_dic['Ar3']        = r'$12 + log\left(\nicefrac{Ar^{2+}}{H^{+}}\right)$'
headers_dic['Ar4']         = r'$12 + log\left(\nicefrac{Ar^{3+}}{H^{+}}\right)$'
varsNum = len(headers_dic)
headers_format = ['HII Galaxy'] + headers_dic.values()

# Import functions
dz = Dazer()
specS = SpectraSynthesizer()

# Declare data location
root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'  # root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
article_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\tables\\'
whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'  # whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'

# Import data
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF(whtSpreadSheet)

# Quick indexing
dz.quick_indexing(catalogue_df)

# Sample objects
excludeObjects = ['SHOC579', 'SHOC575_n2', '11', 'SHOC588', 'SDSS3', 'SDSS1', 'SHOC36']  # SHOC579, SHOC575, SHOC220, SHOC588, SHOC592, SHOC036
sampleObjects = catalogue_df.loc[dz.idx_include & ~catalogue_df.index.isin(excludeObjects)].index.values

# Generate pdf
tableAddress = article_folder + 'ionicAbundanceArS'
# print('Creating table in {}'.format(tableAddress))
# dz.create_pdfDoc(tableAddress, pdf_type='table')
# dz.pdfDoc.packages.append(Package('nicefrac'))
dz.pdf_insert_table(headers_format)

# Loop through the objects
for i in range(sampleObjects.size):

    # Object references
    objName = sampleObjects[i]
    local_reference = objName.replace('_', '-')
    quick_reference = catalogue_df.loc[objName].quick_index
    print '- Treating object {}: {} {}'.format(i, objName, quick_reference)

    # Declare configuration file
    objectFolder = '{}{}/'.format(root_folder, objName)  # '{}{}\\'.format(root_folder, objName)
    dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
    obsData = specS.load_obsData(dataFileAddress, objName)

    # Load observational data
    row_i = [quick_reference] + ['-'] * varsNum
    keys_list = headers_dic.keys()
    for j in range(len(keys_list)):
        item = keys_list[j]
        row_i[j+1] = checkDictValue(obsData, item)

    dz.addTableRow(row_i, last_row=False if sampleObjects[-1] != objName else True, rounddig=3, rounddig_er=1)

# dz.generate_pdf()
dz.generate_pdf(output_address=tableAddress)
