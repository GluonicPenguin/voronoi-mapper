"""
Main file for reading in csv files and creating Voronoi maps
Produces a pdf output plot by default, png supported
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

pd.set_option('display.max_rows', None)

def process_headers(input_df):
  # rename headers based on order to format that the script can read
  renamed_df = input_df.set_axis(['Label', 'Y-Coord', 'X-Coord', 'Colour'], axis=1)

  return renamed_df

def magnify_on(input_df, label):
  # set "label" as centre-point, and magnify other points proportional to absolute distance from it
  coord_pair = [input_df.loc[input_df['Label'] == label, 'X-Coord'].iloc[0], input_df.loc[input_df['Label'] == label, 'Y-Coord'].iloc[0]]
  input_df['X-Diff'] = input_df['X-Coord'] - coord_pair[0]
  input_df['Y-Diff'] = input_df['Y-Coord'] - coord_pair[1]
  # define metric as square of difference and use 1/metric as multiplier for coord values
  input_df['absolute_diff'] = input_df['X-Diff']**2 + input_df['Y-Diff']**2
  input_df[['X-Coord', 'Y-Coord']] = input_df[['X-Coord'], 'Y-Coord']] / input_df['absolute_diff']
  input_df = input_df.drop(['X-Diff', 'Y-Diff', 'absolute_diff'], axis=1, inplace=True)
  
  return input_df

def process_coords(input_df):
  # convert subset coords from input csv to numpy array
  coords = input_df[['X-Coord', 'Y-Coord']].values
  # add dummy rows to array
  coords = np.append(coords, [[999,999], [-999,999], [999,-999], [-999,-999]], axis = 0)

  return coords

def process_colours(input_df):
  # add dummy rows to array
  colourFlag = np.append(input_df[['Colour']].values, [['N'], ['N'], ['N'], ['N']], axis = 0).flatten()
  # assign a random colour to the array if visited, leave white if not
  r = lambda: random.randint(0,255)
  colours = list(map(lambda flag: '#%02X%02X%02X' % (r(),r(),r()) if (flag == 'Y') else 'w', colourFlag))

  return colours

def main(incsv, outplot, plot_type, fisheye):
  # read places, with lat and lon
  places = pd.read_csv(incsv)

  # rename headers based on order to format that the script can read
  new_places = process_headers(places)
  
  # magnify latitude and longitude based on a place name
  if fisheye != "":
    new_places = magnify_on(new_places, fisheye)
    
  # convert subset coords from input csv to numpy array, add dummy rows
  coords = process_coords(new_places)

  # compute voronoi tesselation
  vor = Voronoi(coords)

  # assign a random colour to the array if visited, leave white if not
  colours = process_colours(new_places)

  # plot voronoi diagram
  fig = plt.figure(figsize=(20,16))
  ax = fig.add_subplot(111)
  voronoi_plot_2d(vor, show_vertices = False, ax=ax)
  #ax.imshow(ndimage.rotate(img, 90))
  #plt.figure(figsize=(12,8))

  # colour in the regions
  for j in range(len(coords)):
    region = vor.regions[vor.point_region[j]]
    if not -1 in region:
      polygon = [vor.vertices[i] for i in region]
      plt.fill(*zip(*polygon), colours[j])

  # fix the range of axes, plot locations
  plt.plot(coords[:,0], coords[:,1], 'ko')
  plt.xlim([new_places['X-Coord'].min() - 0.6, new_places['X-Coord'].max() + 0.6]), plt.ylim([new_places['Y-Coord'].min() - 0.6, new_places['Y-Coord'].max() + 0.6])

  # annotate each point with the place name
  [plt.annotate(new_places['Label'][i], (coords[i,0], coords[i,1]), xytext=(coords[i,0]-0.1, coords[i,1]+0.1), fontsize=12) for i in range(len(new_places))]
  fig.savefig(outplot + "." + plot_type, format=plot_type, bbox_inches='tight')
  print("SAVED: " + outplot + "." + plot_type)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("incsv", type=str, help="Input csv file listing places and coords")
    parser.add_argument("outplot", type=str, help="Output plot name and path")
    parser.add_argument("-p", "--plot_type", type=str, default="png", help="Plot format type, e.g. pdf, png, dpi (default png)")
    parser.add_argument("-f", "--fisheye", type=str, default="", help="Magnify points closest to a place like a fisheye")
    args = parser.parse_args()

    main(args.incsv, args.outplot, args.plot_type, args.fisheye)
