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

def process_coords(places):
  # convert subset coords from input csv to numpy array
  coords = places[['Longitude','Latitude']].values
  # add dummy rows to array
  coords = np.append(coords, [[999,999], [-999,999], [999,-999], [-999,-999]], axis = 0)

  return coords

def process_colours(places):
  # add dummy rows to array
  colourFlag = np.append(places[['Been']].values, [['N'], ['N'], ['N'], ['N']], axis = 0).flatten()
  # assign a random colour to the array if visited, leave white if not
  r = lambda: random.randint(0,255)
  colours = list(map(lambda flag: '#%02X%02X%02X' % (r(),r(),r()) if (flag == 'Y') else 'w', colourFlag))

  return colours

def main(incsv, outplot, plot_type):
  # read places, with lat and lon
  places = pd.read_csv(incsv)

  # convert subset coords from input csv to numpy array, add dummy rows
  coords = process_coords(places)

  # compute voronoi tesselation
  vor = Voronoi(coords)

  # assign a random colour to the array if visited, leave white if not
  colours = process_colours(places)

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
  plt.xlim([places['Longitude'].min() - 0.6, places['Longitude'].max() + 0.6]), plt.ylim([places['Latitude'].min() - 0.6, places['Latitude'].max() + 0.6])

  # annotate each point with the place name
  [plt.annotate(places['Place'][i], (coords[i,0], coords[i,1]), xytext=(coords[i,0]-0.1, coords[i,1]+0.1), fontsize=12) for i in range(len(places))]
  fig.savefig(outplot + "." + plot_type, format=plot_type, bbox_inches='tight')
  print("SAVED: " + outplot + "." + plot_type)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("incsv", type=str, help="Input csv file listing places and coords")
    parser.add_argument("outplot", type=str, help="Output plot name and path")
    parser.add_argument("-p", "--plot_type", type=str, default="png", help="Plot format type, e.g. pdf, png, dpi (default png)")
    args = parser.parse_args()

    main(args.incsv, args.outplot, args.plot_type)
