#!/usr/bin/env python
import lineid_plot
from collections import OrderedDict
from dazer_methods import Dazer
from numpy import linspace, zeros, hstack
from scipy.interpolate import interp1d
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import pyplot as plt

#Declare code classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
cHbeta_type             = 'cHbeta_reduc'
nebular_exten           = '_NebularContinuum.fits'
Stellar_ext             = '_StellarContinuum.fits'
emitting_ext            = '_Emission.fits'

#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'legend.fontsize':18, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

#Reddening properties
R_v = 3.4
red_curve = 'G03_average'
cHbeta_type = 'cHbeta_reduc'

obj_lines = {}
obj_lines['SHOC579'] = OrderedDict()
obj_lines['SHOC579'][r'Balmer jump'] = (3646.0, 2.1e-16)
obj_lines['SHOC579'][r'$HI_{11}\lambda3770\AA$'] = (3771.0, 2.1e-16)
obj_lines['SHOC579'][r'$HI_{20}\lambda3683\AA$ '] = (3676.0, 1.85e-16)



ak = lineid_plot.initial_annotate_kwargs()
ak['arrowprops']['relpos'] = (0.5, 0.0)
ak['rotation'] = 90

pk = lineid_plot.initial_plot_kwargs()
pk['linewidth'] = 0.5

#Loop through files
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)
 
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    
    if objName == 'SHOC579':
    
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName)
        fits_file           = catalogue_df.iloc[i].reduction_fits

        #Get reduce spectrum data
        Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
        Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
        Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)
        Wave_E, Int_E, ExtraData_E = dz.get_spectra_data(ouput_folder + objName + emitting_ext)

        #Increase the range of Wave_S so it is greater than the observational range
        Wave_StellarExtension = linspace(3000.0,3399.0,200)
        Int_StellarExtension  = zeros(len(Wave_StellarExtension))

        #Increase the range of Wave_S so it is greater than the observational range
        Int_S   = hstack((Int_StellarExtension, Int_S))
        Wave_S  = hstack((Wave_StellarExtension, Wave_S))

        #Resampling stellar spectra
        Interpolation               = interp1d(Wave_S, Int_S, kind = 'slinear')
        Int_Stellar_Resampled       = Interpolation(Wave_O)

        #Perform the reddening correction
        cHbeta = catalogue_df.iloc[i][cHbeta_type]
        IntObs_dered = dz.derreddening_spectrum(Wave_O, Int_O, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
        IntEmi_dered = dz.derreddening_spectrum(Wave_E, Int_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

        Int_Sum = IntEmi_dered + Int_Stellar_Resampled + Int_N

        dz.data_plot(Wave_O, IntObs_dered, 'Observed spectrum')
        dz.data_plot(Wave_N, Int_N, 'Nebular continuum',linestyle=':')
        dz.data_plot(Wave_S, Int_S, 'Stellar continuum',linestyle='--')
        dz.insert_image('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/SHOC579_invert.png', Image_Coordinates = [0.07,0.875], Zoom=0.25, Image_xyCoords = 'axes fraction')

        #Set titles and legend
        PlotTitle = ''
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle, loc='upper right')

        dz.Axis.set_xlim(3550, 10000)

        axins2 = inset_axes(dz.Axis, width='70%', height='50%', loc=7)


        #sub_axes = plt.axes([6000.0, 1.2e-14, 3000, 3.75e-14])
        #sub_axes.plot(Wave_O, Int_O)
        #sub_axes.set_xlim(3560, 3860)

        # axins2 = zoomed_inset_axes(dz.Axis, zoom=10, loc=7)
        axins2.step(Wave_O, Int_O, label='Observed spectrum') #, linestyle='--', color=colorVector['dark blue'], where = 'mid')
        axins2.step(Wave_N, Int_N, label='Nebular continuum',linestyle=':') #,color=colorVector['orangish'], where = 'mid', linewidth=0.75)
        axins2.step(Wave_S, Int_S, label='Stellar continuum',linestyle='--') #,color=colorVector['orangish'], where = 'mid', linewidth=0.75)
        #
        # mean_flux = Int_O.mean()
        #
        axins2.set_xlim(3560, 3860)
        axins2.set_ylim(2.0e-17, 3.5e-16)
        mark_inset(dz.Axis, axins2, loc1=2, loc2=4, fc="none", ec="0.5")
        #
        axins2.get_xaxis().set_visible(False)
        axins2.get_yaxis().set_visible(False)
        # line_wave       = obj_lines[objName].values()
        # line_label1     = obj_lines[objName].keys()
        # lineid_plot.plot_line_ids(Wave_O, Int_O, line_wave, line_label1, ax = axins2, annotate_kwargs=ak, plot_kwargs=pk)

        for feature in obj_lines[objName]:
            x_coord, y_coord = obj_lines[objName][feature][0], obj_lines[objName][feature][1]
            axins2.text(x_coord, y_coord, feature, {'ha': 'left', 'va': 'bottom'}, rotation=65, fontsize=13)

        #dz.display_fig()
        dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/SHOC579_continua_detail')
#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()
