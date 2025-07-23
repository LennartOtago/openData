import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))

from pathlib import Path
path = Path(cwd) # Path("/here/your/path/file.txt")
parentDir = str( path.parent.absolute())



dir = parentDir + '/openData/'
def plot_he5_data(file_path):
    # Open the .he5 file
    with h5py.File(file_path, 'r') as f:
        # Print out the keys available in the file
        print("Keys in the .he5 file:")
        for key in f.keys():
            print(key)

        # Access the dataset
        dataset = f[dir]  # Replace '/path/to/dataset' with the actual path

        # Read the data
        data = dataset[:]

        # Plot the data
        plt.imshow(data, cmap='viridis')  # You can choose any colormap you prefer
        plt.colorbar(label='Data Values')  # Add a colorbar
        plt.title('MLS Satellite Data')  # Add a title
        plt.xlabel('X Axis')  # Label for X axis
        plt.ylabel('Y Axis')  # Label for Y axis
        plt.show()

# Example usage
#file_path = '/home/lennartgolks/PycharmProjects/openData/MLS-Aura_L2GP-O3_v05-02-c02_2024d085.he5'  # Replace 'path/to/your/file.he5' with the actual file path
#file_path = '/Users/lennart/PycharmProjects/openData/MLS-Aura_L2GP-O3_v05-02-c02_2024d085.he5'
file_path = dir + '/MLS-Aura_L2GP-O3_v05-02-c02_2024d085.he5'
file_path = dir + 'AntarcticRegion/MLS-Aura_L2GP-O3_v05-01-c01_2020d125.he5'
#file_path = dir + 'AntarcticRegion/MLS-Aura_L2GP-O3_v05-00-c01_2009d262.he5'
#file_path = dir + 'AntarcticRegion/MLS-Aura_L2GP-O3_v05-01-c01_2020d199.he5'





def print_h5_structure(file_path, parent='/'):
    with h5py.File(file_path, 'r') as f:
        for key in f[parent].keys():
            print(parent + key)
            if isinstance(f[parent + key], h5py.Group):
                print_h5_structure(file_path, parent + key + '/')


def openDatSet(file_path):
    print_h5_structure(file_path)

    keys = ['/HDFEOS/SWATHS/O3 column/Data Fields/O3 column',
            '/HDFEOS/SWATHS/O3/Geolocation Fields/Pressure',
            '/HDFEOS/SWATHS/O3/Geolocation Fields/Latitude',
            '/HDFEOS/SWATHS/O3/Geolocation Fields/Longitude']

    with h5py.File(file_path, 'r') as f:
        # Access the dataset
        dataset = f['/HDFEOS/SWATHS/O3/Data Fields/L2gpValue']  # Replace '/path/to/dataset' with the actual path
        dataset = f['/HDFEOS/SWATHS/O3/Data Fields/O3']
        # Read the data
        data = dataset[:]#[30,:].squeeze()
        # data[data == dataset.fillvalue] = np.nan
        # data = np.ma.masked_where(np.isnan(data), data)
        # Get attributes needed for the plot.
        # String attributes actually come in as the bytes type and should
        # be decoded to UTF-8 (python3).
        title = dataset.attrs['Title'].decode()
        units = dataset.attrs['Units'].decode()

        # Read the pressure
        pressureset = f['/HDFEOS/SWATHS/O3/Geolocation Fields/Pressure']  # Replace '/path/to/dataset' with the actual path

        pressure = pressureset[:]
        # Get attributes needed for the plot.
        # String attributes actually come in as the bytes type and should
        # be decoded to UTF-8 (python3).
        pressuretitle = pressureset.attrs['Title'].decode()
        pressureunits = pressureset.attrs['Units'].decode()

        # Read the precision
        Prec = f['/HDFEOS/SWATHS/O3/Data Fields/O3Precision']  # Replace '/path/to/dataset' with the actual path

        # Read the data
        O3Prec = Prec[:]

        # Read the precision
        Prec = f['/HDFEOS/SWATHS/O3/Data Fields/O3Precision']  # Replace '/path/to/dataset' with the actual path

        # Read the data
        O3Prec = Prec[:]



        # # Access the dataset
        # datasetLat = f['/HDFEOS/SWATHS/O3 column/Geolocation Fields/Latitude']  # Replace '/path/to/dataset' with the actual path
        #
        # # Read the data
        # dataLat = datasetLat[:]
        # # Handle fill value.
        # dataLat[dataLat == datasetLat.fillvalue] = np.nan
        # dataLat = np.ma.masked_where(np.isnan(dataLat), dataLat)
        #
        # # Access the dataset
        # datasetLong = f['/HDFEOS/SWATHS/O3 column/Geolocation Fields/Longitude']  # Replace '/path/to/dataset' with the actual path
        #
        # # Read the data
        # dataLong = datasetLong[:]
        # # Handle fill value.
        # dataLong[dataLong == datasetLong.fillvalue] = np.nan
        # dataLong = np.ma.masked_where(np.isnan(dataLong), dataLong)
    return data, pressure, title, units, pressuretitle, pressureunits, O3Prec

from os import listdir
from os.path import isfile, join
f = 'MLS-Aura_L2GP-O3_v05-00-c01_2009d262.he5'
f = 'MLS-Aura_L2GP-O3_v05-01-c01_2020d199.he5'
data, pressure, title, units, pressuretitle, pressureunits, O3Prec = openDatSet(dir + 'AntarcticRegion/' + f)
##
O3Prec[O3Prec<0]=0
i = 71
fig, axs = plt.subplots(tight_layout=True)
plt.plot(data[i], pressure)
plt.errorbar(data[i], pressure, xerr=O3Prec[i])
axs.invert_yaxis()
axs.set_yscale('log')
axs.set_ylabel('pressure in' + pressureunits)
axs.set_xlabel('VMR of Ozone')
plt.show()

# i = 121
# fig, axs = plt.subplots(tight_layout=True)
# plt.plot(data[i], pressure)
# plt.errorbar(data[i], pressure, xerr=O3Prec[i])
# axs.invert_yaxis()
# axs.set_yscale('log')
# axs.set_ylabel('pressure in' + pressureunits)
# axs.set_xlabel('VMR of Ozone')
# plt.show()

# for i in range(len(data)):
#     fig, axs = plt.subplots(tight_layout=True)
#     plt.plot(data[i], pressure)
#     plt.errorbar(data[i], pressure, xerr =O3Prec[i])
#     axs.invert_yaxis()
#     axs.set_yscale('log')
#     axs.set_ylabel('pressure in' + pressureunits)
#     axs.set_xlabel('VMR of Ozone')
#     plt.show()

# for f in listdir(dir + 'AntarcticRegion'):
#     print(f)
#     data, pressure, title, units, pressuretitle, pressureunits, dataset = openDatSet(dir + 'AntarcticRegion/' + f)
#     ##
#     fig, axs = plt.subplots(tight_layout=True)
#     plt.plot(data,pressure)
#     axs.invert_yaxis()
#     axs.set_yscale('log')
#     axs.set_ylabel('pressure in' + pressureunits)
#     axs.set_xlabel('VMR of Ozone')
#     plt.show()


#np.savetxt('testProf.txt', [pressure,data[i]], fmt = '%.15f', delimiter= '\t')





print('bla')