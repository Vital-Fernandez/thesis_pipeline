from dazer_methods  import Dazer
from numpy          import nanmean, nanstd, mean, nan as np_nan
from uncertainties  import ufloat, unumpy, umath
import pandas as pd
 
#Generate dazer object
dz = Dazer()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'legend.fontsize':17, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

dz.quick_indexing(catalogue_df)
idcs = (pd.notnull(catalogue_df.OI_HI_emis2nd)) & (pd.notnull(catalogue_df.NI_HI_emis2nd)) & (pd.notnull(catalogue_df.HeII_HII_from_O_emis2nd)) & (catalogue_df.quick_index.notnull()) & (~catalogue_df.index.isin(['SHOC593']))

print 'Contando', len(catalogue_df.index), len( catalogue_df.loc[catalogue_df.quick_index.notnull()].values)

#Prepare data
O_values  = catalogue_df.loc[idcs].OI_HI_emis2nd.values 
N_values  = catalogue_df.loc[idcs].NI_HI_emis2nd.values
HeII_HI   = catalogue_df.loc[idcs].HeII_HII_from_O_emis2nd.values 
objects   = catalogue_df.loc[idcs].quick_index.values

N_O_ratio = N_values/O_values

for i in range(len(objects)):
    print objects[i], '\t', N_O_ratio[i], '\t', umath.log10(N_O_ratio[i])

dz.data_plot(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), label = '', markerstyle='o', x_error=unumpy.std_devs(HeII_HI), y_error=unumpy.std_devs(N_O_ratio))
dz.plot_text(unumpy.nominal_values(HeII_HI), unumpy.nominal_values(N_O_ratio), text=objects, x_pad=1.005, y_pad=1.01)

dz.FigWording(r'y', r'$N/O$', r'Nitrogen to oxygen ratio versus helium abundance')
dz.display_fig()

#dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/Images/NO_to_y')

